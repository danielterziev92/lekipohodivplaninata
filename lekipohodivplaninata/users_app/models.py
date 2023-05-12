from cloudinary import models as cloudinary_models
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.users_app.manager import UserAppManager


class UserApp(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Email',
        error_messages={
            'unique': _('Моля използвайте по-сложна парола.'),
        }
    )

    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name='Служител'
    )

    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name='Активен'
    )

    data_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserAppManager()

    class Meta:
        verbose_name = 'Потребител'
        verbose_name_plural = 'Потребители'

    def __str__(self):
        return self.email


class BaseProfile(models.Model):
    FIRST_NAME_MAX_LENGTH = 25
    LAST_NAME_MAX_LENGTH = 25

    user_id = models.OneToOneField(
        UserApp,
        primary_key=True,
        on_delete=models.RESTRICT,
        verbose_name='Потребител'
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Име',
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Фамилия',
    )

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = 'Профили'


class GuideProfile(models.Model):
    AVATAR_DIRECTORY = 'images/guides/avatars/'
    CERTIFICATE_DIRECTORY = 'images/guides/certificates/'

    user_id = models.OneToOneField(
        UserApp,
        primary_key=True,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        verbose_name='Потребител'
    )

    profile_id = models.OneToOneField(
        BaseProfile,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        verbose_name='Профил'
    )

    avatar = cloudinary_models.CloudinaryField(
        null=False,
        blank=False,
        verbose_name='Профилна снимка'
    )

    date_of_birth = models.DateField(
        null=False,
        blank=False,
        verbose_name='Дата на раждане'
    )

    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание'
    )

    certificate = cloudinary_models.CloudinaryField(
        null=False,
        blank=False,
        verbose_name='Сертификат'
    )

    class Meta:
        verbose_name_plural = 'Водачи'
