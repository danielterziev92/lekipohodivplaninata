from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

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

    signed_on = models.DateTimeField(
        auto_now_add=True,
    )


class SiteEvaluation(models.Model):
    assessment = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=(ValueInRangeValidator(1, 10),)
    )

    comment = models.TextField(
        null=True,
        blank=True,
    )

    rated_in = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )


class HikeEvaluation(models.Model):
    assessment = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=(ValueInRangeValidator(1, 10),)
    )

    comment = models.TextField(
        null=True,
        blank=True,
    )

    user_id = models.ForeignKey(
        BaseProfile,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    hike_id = models.ForeignKey(
        Hike,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )
