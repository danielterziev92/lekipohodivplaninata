from django import forms
from django.contrib.auth import forms as auth_form, get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.users_app.models import ProfileBaseInformation

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
        )
    )

    password = forms.CharField(
        strip=False,
        label='Парола:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Въведете парола',
                'autocomplete': 'current-password',
            }),
    )


class SignUpForm(auth_form.UserCreationForm):
    email = forms.EmailField(
        label='Имейл:',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Въведете вашият имейл',
                'autocomplete': 'email',
            }),
    )

    first_name = forms.CharField(
        max_length=25,
        # error_messages='Моля въведете името си на кирилица',
        help_text='Моля въведете вашето име',
        label='Име:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Въведете вашето име'
            })
    )

    last_name = forms.CharField(
        max_length=25,
        label='Фамилия:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Въведете вашета фамилия'
            })
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
            'password_too_similar': _('Паролата ви е много подобна с имейла.'),
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
            'password_too_similar': _('Паролата ви е много подобна с имейла.'),
        }
        # help_text=_("Enter the same password as before, for verification."),
    )

    error_messages = {
        'required': _('Полето е задължително'),
        "password_mismatch": _("Паролите не съвпадат!"),
        'password_too_similar': _('Паролата ви е много подобна с имейла.'),
    }

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password1', 'password2', 'first_name', 'last_name')
        label = {
            UserModel.USERNAME_FIELD: 'Имейл',
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
