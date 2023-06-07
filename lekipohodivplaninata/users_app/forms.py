import datetime

from cloudinary import forms as cloudinary_form
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_form, get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile
from lekipohodivplaninata.users_app.models import UserApp

UserModel = get_user_model()


class UserModelForm(forms.ModelForm):
    email = forms.EmailField(
        label='Имейл',
        widget=forms.EmailInput(
            attrs={
                'id': 'id_email',
                'autocomplete': 'email',
                'data-url': "/domain/email_autocomplete/",
            }
        ),
    )

    class Meta:
        model = UserModel
        exclude = '__all__'
        error_messages = {
            'required': 'Това поле е задължитено',
        }


class BaseUserModelForm(forms.ModelForm):
    PHONE_NUMBER_MAX_LENGTH = 14

    first_name = forms.CharField(
        max_length=BaseProfile.FIRST_NAME_MAX_LENGTH,
        label='Име',
        widget=forms.TextInput(),
    )

    last_name = forms.CharField(
        max_length=BaseProfile.LAST_NAME_MAX_LENGTH,
        label='Фамилия',
        widget=forms.TextInput(),
    )

    phone_number = forms.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        label='Телефон',
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'pattern': '[+]?[0-9]{10,13}',
                'minlength': 10,
            }),
    )

    class Meta:
        model = BaseProfile
        exclude = '__all__'


class BaseUserUpdateForm(BaseUserModelForm):
    class Meta:
        model = BaseProfile
        fields = ('first_name', 'last_name', 'phone_number')


class SignInForm(auth_form.AuthenticationForm):
    username = forms.EmailField(
        label='Имейл',
        widget=forms.EmailInput(
            attrs={
                'id': 'id_email',
                'autocomplete': 'email',
                'data-url': "/domain/email_autocomplete/",
            }
        ),
    )

    password = forms.CharField(
        strip=False,
        label='Парола:',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
            }),
    )

    def clean_username(self):
        email = self.cleaned_data.get('username').lower()
        if not UserApp.objects.filter(email=email):
            raise ValidationError('Потребител с този имейл не съществува')

        return email

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(self.request, username=email, password=password)

            if user is None:
                self.add_error('password', 'Невалидена парола.')
                raise self.get_invalid_login_error()

            super().clean()


class SignUpFormUser(UserModelForm, BaseUserModelForm, auth_form.UserCreationForm):
    password1 = forms.CharField(
        label='Парола',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'id': 'password_1',
            }),
        error_messages={
            'password_too_similar': 'Паролата ви е много близка с имейла.'
        },
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label='Повторете:',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'id': 'password_2',
            }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserApp.objects.filter(email=email):
            self.add_error('email', 'Потребител с този имейл вече съществува')

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            self.add_error('password2', 'Паролите се различават')

        return password2

    def save(self, commit=True):
        try:
            with transaction.atomic():
                user = super().save(commit=commit)

                profile = BaseProfile(
                    user_id=user,
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    phone_number=self.cleaned_data['phone_number'],
                )

                if commit:
                    profile.save()
        except Exception:
            raise ValidationError('Нещо се обърка')

        return user

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2', 'first_name', 'last_name', 'phone_number')
        label = {
            UserModel.USERNAME_FIELD: 'Имейл',
        }
        error_messages = {
            'password_mismatch': _('Паролите не съвпадат!'),
            'required': _('Полето е задължително'),
        }


class GuideProfileFormUser(BaseUserModelForm, forms.ModelForm):
    avatar = cloudinary_form.CloudinaryFileField(
        label='Профилана снимка',
        options={
            'folder': 'guides/avatars/'
        },
        required=False,
    )

    date_of_birth = forms.DateField(
        label='Дата на раждане',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea()
    )

    certificate = cloudinary_form.CloudinaryFileField(
        label='Сертификат',
        options={
            'folder': 'guides/certificates/'
        },
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['value'] = kwargs.get('instance').profile_id.first_name
        self.fields['last_name'].widget.attrs['value'] = kwargs.get('instance').profile_id.last_name

    class Meta:
        model = GuideProfile
        fields = ('first_name', 'last_name', 'avatar', 'date_of_birth', 'description', 'certificate')

    def save(self, commit=True):
        guide_profile = super().save(commit=commit)

        profile = BaseProfile(
            user_id=self.instance.user_id,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

        if commit:
            profile.save()

        return guide_profile


class UserResetPasswordForm(auth_form.PasswordResetForm):
    domain = 'lekipohodivplaninata.bg'
    site_name = 'ЛекиПоходиВпланината.BG'

    email = forms.EmailField(
        label='Имейл'
    )

    def send_mail(self, subject_template_name,
                  email_template_name,
                  context,
                  from_email,
                  to_email,
                  html_email_template_name=None,
                  ):
        context['domain'] = self.domain
        context['site_name'] = self.site_name

        return super().send_mail(
            subject_template_name, email_template_name,
            context, from_email, to_email, html_email_template_name,
        )

    def save(self, **kwargs):
        kwargs['extra_email_context'] = {
            'ip_address': self.get_ip_address(kwargs['request']),
            'time_remaining': self.get_time_remaining
        }
        super().save(**kwargs)

    @staticmethod
    def get_ip_address(request):
        return request.META['REMOTE_ADDR']

    @property
    def get_time_remaining(self):
        return (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%m-%d-%Y %H:%M:%S')


class UserSetPasswordForm(auth_form.SetPasswordForm):
    new_password1 = forms.CharField(
        label=_('Нова парола'),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'id': 'password_1',
            }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_('Повтори'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'id': 'password_2'
            }),
    )

    class Meta:
        error_messages = {
            'password_mismatch': _('Паролите не съвпадат'),
        }
