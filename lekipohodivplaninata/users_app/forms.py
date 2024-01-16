from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_form, get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.cache import cache
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
    MESSAGES = {
        'user_does_not_exist': 'Потребител с този имейл не съществува.',
        'invalid_password': 'Невалидена парола.',
    }

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
            raise ValidationError(self.MESSAGES['user_does_not_exist'])

        return email

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(self.request, username=email, password=password)

            if user is None:
                self.add_error('password', self.MESSAGES['invalid_password'])
                raise self.get_invalid_login_error()

            super().clean()


class SignUpFormUser(UserModelForm, BaseUserModelForm, auth_form.UserCreationForm):
    MESSAGES = {
        'password_too_similar': 'Паролата ви е много близка с имейла.',
        'password_mismatch': 'Паролите се различават.',
        'user_already_exists': 'Потребител с този имейл вече съществува.',
        'successful_registration': 'Регистрацията мина успешно!',
        'something_went_wrong': 'Нещо се обърка, моля опитайте отново.',
    }

    password1 = forms.CharField(
        label='Парола',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'id': 'password_1',
            }),
        error_messages={
            'password_too_similar': MESSAGES['password_too_similar']
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
        email = self.cleaned_data.get('email').lower()
        if UserApp.objects.filter(email=email):
            self.add_error('email', self.MESSAGES['user_already_exists'])

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            self.add_error('password2', self.MESSAGES['password_mismatch'])

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

                messages.success(self._request, self.MESSAGES['successful_registration'])
        except Exception:
            messages.error(self._request, self.MESSAGES['something_went_wrong'])
            return

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
    avatar = forms.ImageField(
        label='Профилана снимка',
        widget=forms.FileInput,
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

    certificate = forms.ImageField(
        label='Сертификат',
        widget=forms.FileInput,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['value'] = kwargs.get('instance').profile_id.first_name
        self.fields['last_name'].widget.attrs['value'] = kwargs.get('instance').profile_id.last_name
        self.fields['phone_number'].widget.attrs['value'] = kwargs.get('instance').profile_id.phone_number

    class Meta:
        model = GuideProfile
        fields = ('first_name', 'last_name', 'avatar', 'date_of_birth', 'description', 'certificate', 'phone_number')

    def save(self, commit=True):
        guide_profile = super().save(commit=commit)

        profile = BaseProfile(
            user_id=self.instance.user_id,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
        )

        if commit:
            profile.save()

        return guide_profile


class UserResetPasswordForm(auth_form.PasswordResetForm):
    MESSAGE = {
        'email_does_not_exist': 'Потребител с този имейл не съществува',
        'successful_send_email': 'Вече има изпратена завка за смяна на паролата',
    }

    email = forms.EmailField(
        label='Имейл',
        widget=forms.EmailInput(),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserModel.objects.filter(email=email):
            self.add_error('email', self.MESSAGE['email_does_not_exist'])

        if cache.get(email):
            self.add_error('email', self.MESSAGE['successful_send_email'])

        return email


class UserSetPasswordForm(auth_form.SetPasswordForm):
    MESSAGE = {
        'password_mismatch': 'Паролите не съвпадат.',
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

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('password_1')
        password2 = self.cleaned_data.get('password_2')
        if password1 != password2:
            self.add_error('new_password2', self.MESSAGE['password_mismatch'])

    class Meta:
        error_messages = {
            'password_mismatch': _('Паролите не съвпадат'),
        }
