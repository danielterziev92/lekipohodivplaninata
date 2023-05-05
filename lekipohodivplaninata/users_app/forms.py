from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_form, get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.users_app.models import ProfileBaseInformation, UserApp

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
        max_length=25,
        # error_messages='Моля въведете името си на кирилица',
        help_text='Моля въведете вашето име',
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
        max_length=25,
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
                'autocomplete': 'current-password'
            }),
        strip=False,
        error_messages={
            'required': _('Полето е задължително'),
            'password_too_similar': 'Паролата ви е много близка с имейла.'
        },
        help_text={
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

        profile = ProfileBaseInformation(
            user_id=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

        if commit:
            profile.save()

        return user


class UserResetPasswordForm(auth_form.PasswordResetForm):
    email = forms.EmailField(
        label='Имейл'
    )

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        context['domain'] = 'lekipohodivplaninata.bg'
        context['site_name'] = 'ЛекиПоходиВпланината.BG'
        context['user_full_name'] = context['user'].profilebaseinformation.get_full_name
        return super().send_mail(subject_template_name, email_template_name, context, from_email, to_email,
                                 html_email_template_name)