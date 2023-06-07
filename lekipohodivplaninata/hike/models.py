from django.db import models
from cloudinary import models as cloudinary_models
from django.utils.safestring import mark_safe

from lekipohodivplaninata.hike.validators import before_today_validator
from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile


class AuditInfoMixin(models.Model):
    created_on = models.DateField(
        auto_now_add=True
    )

    updated_on = models.DateField(
        auto_now=True
    )

    class Meta:
        abstract = True


class HikeType(models.Model):
    TITLE_MAX_LENGTH = 30

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Заглавие',
        help_text='Моля попълнете типа на похода'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип поход'
        verbose_name_plural = 'Типове походи'


class HikeLevel(models.Model):
    TITLE_MAX_LENGTH = 30

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Заглавие',
        help_text='Моля попълнете вида трудност'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ниво на поход'
        verbose_name_plural = 'Нива на походи'


class HikeMorePicture(models.Model):
    image = cloudinary_models.CloudinaryField(
        null=True,
        blank=True,
        verbose_name='Снимка'
    )

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'снимка'
        verbose_name_plural = 'Допълнителни снимки към походи'


class Hike(AuditInfoMixin, models.Model):
    TITLE_MAX_LENGTH = 30
    DESCRIPTION_MAX_LENGTH = 30
    DURATION_MAX_LENGTH = 20
    PICTURE_DIRECTORY = 'treks-pictures'

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Заглавие',
        help_text='Моля попълнете заглавие на похода',
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    type = models.ForeignKey(
        HikeType,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание',
        help_text='Моля попълнете описание за похода',
    )

    level = models.ForeignKey(
        HikeLevel,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        verbose_name='Ниво на похода',
        help_text='Моля изберете ниво за похода',
    )

    duration = models.CharField(
        max_length=DURATION_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Продължителност',
        help_text='Моля попълнете продължителността на похода в цифри',
    )

    event_date = models.DateField(
        null=False,
        blank=False,
        verbose_name='Дата на похода',
        help_text='Моля изберете дата за похода',
        validators=(before_today_validator,)
    )

    price = models.DecimalField(
        default=0.00,
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена',
        help_text='Моля попълнете само цифрата на сумата за похода'
    )

    main_picture = cloudinary_models.CloudinaryField(
        null=False,
        blank=False,
        verbose_name='Основна снимка',
        help_text='Тук трябва добавите основна снимка за похода',
    )

    more_pictures = models.ManyToManyField(
        HikeMorePicture,
        null=True,
        blank=True,
        verbose_name='Допълнителни снимки',
        help_text='Тук можете да добавите допълнителни снимки за похода',
    )

    @property
    def get_hike_price(self):
        return f'{self.price} лв.'

    @property
    def get_main_picture(self):
        return mark_safe(f'<img src="{self.main_picture.url}" style="max-width: 300px;"/>')

    @property
    def get_thumbnail_image(self):
        return mark_safe(f'<img src="{self.main_picture.url}" style="max-width: 50px"/>')

    @property
    def get_duration_time(self):
        return f'{self.duration} часа'

    @property
    def get_event_date(self):
        return self.event_date.strftime('%d/%m/%Y')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'поход'
        verbose_name_plural = 'Походи'


class HikeAdditionalInfo(models.Model):
    EVENT_VENUE_MAX_LENGTH = 30
    DEPARTURE_PLACE_MAX_LENGTH = 30

    hike_id = models.OneToOneField(
        Hike,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    event_venue = models.CharField(
        max_length=EVENT_VENUE_MAX_LENGTH,
        null=False,
        blank=False,
    )

    departure_time = models.TimeField(
        null=False,
        blank=False,
    )

    departure_place = models.CharField(
        max_length=DEPARTURE_PLACE_MAX_LENGTH,
        null=False,
        blank=False,
    )
