from django.db import models


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


class HikeMorePicture(models.Model):
    picture = models.ImageField(
        upload_to='hikes-more-pictures'
    )


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
        on_delete=models.RESTRICT
    )

    duration = models.CharField(
        max_length=DURATION_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Продължителност',
        help_text='Моля попълнете продължителността на похода',
    )

    event_date = models.DateField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена',
        help_text='Моля попълнете само цифрата на сумата за похода'
    )

    main_picture = models.ImageField(
        upload_to='hike-main-pictures'
    )

    more_pictures = models.ManyToManyField(
        HikeMorePicture
    )

    @property
    def get_hike_price(self):
        return f'{self.price} лв.'
