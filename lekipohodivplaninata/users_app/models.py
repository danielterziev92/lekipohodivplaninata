from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.db import models

from lekipohodivplaninata.users_app.manager import UserAppManager


class UserApp(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Email',
        help_text='Моля, попълнете email.'
    )

    is_staff = models.BooleanField(
        # _('Staff Status'),
        default=False,
        null=False,
        blank=False
    )

    data_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserAppManager()

    class Meta:
        verbose_name_plural = 'Потребители'


class ProfileBaseInformation(models.Model):
    user_id = models.OneToOneField(
        UserApp,
        primary_key=True,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='Име',
        help_text='Моля попълнете вашето име',
    )

    last_name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='Фамилия',
        help_text='Моля попълнете вашата фамилия',
    )

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = 'Профили'
