from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from cloudinary import models as cloudinary_models

from lekipohodivplaninata.core.validators import ValueInRangeValidator
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile

BaseUserModel = BaseProfile
HikeModel = Hike


class Choices:
    def __init__(self, *args):
        self.choices = args

    def get_all_choices(self):
        return tuple((ind, choice) for ind, choice in enumerate(self.choices))


class SignUpForHike(models.Model):
    TRAVEL_CHOICES = Choices('Организиран Транспорт', 'Собствен Транспорт')

    hike_id = models.ForeignKey(
        HikeModel,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    user_type = models.ForeignKey(
        ContentType,
        on_delete=models.RESTRICT
    )

    user_id = models.PositiveIntegerField()

    user_object = GenericForeignKey('user_type', 'user_id')

    travel_with = models.PositiveSmallIntegerField(
        choices=TRAVEL_CHOICES.get_all_choices(),
        null=False,
        blank=False,
    )

    adults_numbers = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    children_numbers = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    is_confirmed = models.BooleanField(
        null=True,
        blank=True,
    )

    is_presence = models.BooleanField(
        null=True,
        blank=True,
    )

    signed_on = models.DateTimeField(
        auto_now_add=True,
    )


class Evaluation(models.Model):
    assessment = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=(ValueInRangeValidator(1, 10),)
    )

    comment = models.TextField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class SiteEvaluation(Evaluation):
    rated_in = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )


class HikeEvaluationUsers(models.Model):
    user_id = models.ForeignKey(
        BaseProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )


class HikeEvaluation(Evaluation):
    SLUG_LENGTH = 40

    assessment = models.PositiveSmallIntegerField(
        null=True,
        blank=False,
        validators=(ValueInRangeValidator(1, 10),)
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    hike_id = models.ForeignKey(
        Hike,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    users = models.ManyToManyField(
        to=HikeEvaluationUsers,
    )


class Slider(models.Model):
    image = cloudinary_models.CloudinaryField(
        null=False,
        blank=False,
        verbose_name='Снимка',
        help_text='Тук трябва добавите основна снимка за похода',
    )

    hike_id = models.OneToOneField(
        to=Hike,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        verbose_name='Изберете поход',
        help_text='Моля изберете един от посочениет походи',
    )


class SocialMedia(models.Model):
    NAME_MAX_LENGTH = 20
    FONTAWESOME_MAX_LENGTH = 50
    ICON_COLOR_MAX_LENGTH = 6

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    url = models.URLField(
        null=False,
        blank=False,
    )

    fontawesome_icon = models.CharField(
        max_length=FONTAWESOME_MAX_LENGTH,
        null=True,
        blank=True,
    )

    icon_color = models.CharField(
        max_length=ICON_COLOR_MAX_LENGTH,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Социална медия'
        verbose_name_plural = 'Социални медии'


class Settings(models.Model):
    PHONE_NUMBER_MAX_LENGTH = 13

    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Телефон за контакт',
        help_text='Моля въведете телефон за контакт с вас'
    )

    email_for_contact = models.EmailField(
        null=False,
        blank=False,
        verbose_name='Емейл за контакт',
        help_text='Моля въведете емайла с когото ще могат да се свързват с вас'
    )

    social_media = models.ManyToManyField(
        to=SocialMedia,
        blank=True,
    )

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
