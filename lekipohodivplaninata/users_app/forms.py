import datetime

from cloudinary import forms as cloudinary_form
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_form, get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile

UserModel = get_user_model()


class SignInForm(auth_form.AuthenticationForm):
    username = forms.EmailField(
        label='Имейл',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Въведете вашият имейл',
                'id': 'id_email',
                'autocomplete': 'email',
                'data-url': "/domain/email_autocomplete/",
            }
        ),
        error_messages={
            'required': 'Това поле е задължитено',
        }
    )

    password = forms.CharField(
        strip=False,
        label='Парола:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Въведете парола',
                'autocomplete': 'current-password',
            }),
        error_messages={
            'required': _('Полето е задължително'),
        },
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(self.request, username=email, password=password)

            if user is None:
                self.add_error('username', 'Невалиден имейл или парола.')
                raise self.get_invalid_login_error()

            super().clean()


class SignUpForm(auth_form.UserCreationForm):
    email = forms.EmailField(
        label='Имейл:',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Въведете вашият имейл',
                'autocomplete': 'email',
            }),
        error_messages={
            'required': _('Полето е задължително'),
        }
    )

    first_name = forms.CharField(
        max_length=BaseProfile.FIRST_NAME_MAX_LENGTH,
        label='Име:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Въведете вашето име'
            }),
        error_messages={
            'required': _('Полето е задължително'),
        }
    )

    last_name = forms.CharField(
        max_length=BaseProfile.LAST_NAME_MAX_LENGTH,
        label='Фамилия:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Въведете вашета фамилия'
            }),
        error_messages={
            'required': _('Полето е задължително'),
        }
    )

    password1 = forms.CharField(
        label=_("Парола:"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Въведете парола',
                'autocomplete': 'current-password',
                'id': 'password_1',
            }),
        error_messages={
            'required': _('Полето е задължително'),
            'password_too_similar': 'Паролата ви е много близка с имейла.'
        },
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("Повторете:"),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторете вашата парола',
                'autocomplete': 'current-password',
                'id': 'password_2',
            }),
        strip=False,
        error_messages={
            'required': _('Полето е задължително'),
            'password_too_similar': 'Паролата ви е много близка с имейла.'
        },
    )

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2', 'first_name', 'last_name')
        label = {
            UserModel.USERNAME_FIELD: 'Имейл',
        }
        error_messages = {
            "password_mismatch": _("Паролите не съвпадат!"),
            'password_too_similar': _('Паролата ви е много подобна с имейла.'),

        }

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = BaseProfile(
            user_id=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

        if commit:
            profile.save()

        return user


class GuideProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=BaseProfile.FIRST_NAME_MAX_LENGTH,
        label='Име',
    )

    last_name = forms.CharField(
        max_length=BaseProfile.LAST_NAME_MAX_LENGTH,
        label='Фамилия',
    )

    avatar = cloudinary_form.CloudinaryFileField(
        label='Профилана снимка',
        widget={

        },
        options={
            'tags': "directly_uploaded",
            'crop': 'limit', 'width': 1000, 'height': 1000,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 100}],
            'folder': 'guides/avatars/'
        },
        required=False,
    )

    date_of_birth = forms.DateField(
        label='Дата на раждане',

    )

    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea()
    )

    certificate = cloudinary_form.CloudinaryFileField(
        label='Сертификат',
        options={
            'tags': "directly_uploaded",
            'crop': 'limit', 'width': 1000, 'height': 1000,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 100}],
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
        labels = {
            'avatar': 'Профилна снимка',
            'certificate': 'Сертификат',
        }


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
    error_messages = {
        'password_mismatch': _('Паролите не съвпадат'),
    }

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
