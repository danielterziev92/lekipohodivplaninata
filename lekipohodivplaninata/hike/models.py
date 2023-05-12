from django.db import models
from cloudinary import models as cloudinary_models


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
    PICTURE_DIRECTORY = 'image/hikes-more-picture'

    picture = cloudinary_models.CloudinaryField(
        null=True,
        blank=True,
        verbose_name='Снимка'
    )

    class Meta:
        verbose_name = 'Допълнителни снимки към поход'
        verbose_name_plural = 'Допълнителни снимки към походи'


class Hike(AuditInfoMixin, models.Model):
    TITLE_MAX_LENGTH = 30
    DESCRIPTION_MAX_LENGTH = 30
    DURATION_MAX_LENGTH = 20

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Заглавие',
        help_text='Моля попълнете заглавие на похода',
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
        verbose_name='Ниво на похода',
        help_text='Моля изберете ниво за похода',
    )

    duration = models.CharField(
        max_length=DURATION_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Продължителност',
        help_text='Моля попълнете продължителността на похода',
    )

    event_date = models.DateField(
        verbose_name='Дата на похода',
        help_text='Моля изберете дата за похода',
    )

    price = models.DecimalField(
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
        verbose_name='Допълнителни снимки',
        help_text='Тук можете да добавите допълнителни снимки за похода',
    )

    @property
    def get_hike_price(self):
        return f'{self.price} лв.'

    class Meta:
        verbose_name = 'Поход'
        verbose_name_plural = 'Походи'
