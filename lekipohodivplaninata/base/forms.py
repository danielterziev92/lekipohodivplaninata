from django import forms
from django.contrib.auth import get_user_model, login
from django.contrib.contenttypes.models import ContentType
from django.db import ProgrammingError
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.base.models import SignUpForHike, SiteEvaluation, HikeEvaluation, Slider
from lekipohodivplaninata.core.mixins import UserDataMixin, PicturesMixin
from lekipohodivplaninata.core.validators import ValueInRangeValidator
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import AnonymousAppUser, BaseProfile

UserModel = get_user_model()


def check_is_digit(value):
    return int(value) if value.isdecimal() else None


class SignUpHikeForm(UserDataMixin, forms.ModelForm):
    PHONE_NUMBER_MAX_LENGTH = 14
    PHONE_NUMBER_MIN_LENGTH = 10
    try:
        hikes = tuple(Hike.objects.all().values_list('id', 'title'))
    except ProgrammingError:
        hikes = tuple()

    travel_with = tuple(SignUpForHike.TRAVEL_CHOICES.get_all_choices())

    first_name = forms.CharField(
        label='Име',
        widget=forms.TextInput(
            attrs={
                'id': 'first-name',
            }
        )
    )

    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={
                'id': 'last-name',
            }
        )
    )

    phone_number = forms.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        label='Телефон',
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'pattern': '[+]?[0-9]{10,13}',
                'minlength': PHONE_NUMBER_MIN_LENGTH,
            }),
    )

    adults_numbers = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'value': 0,
                'inputmode': 'numeric'
            }
        )
    )

    children_numbers = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'value': 0,
                'inputmode': 'numeric'
            }
        )
    )

    choose_hike = forms.ChoiceField(
        label='Избери поход',
        choices=hikes
    )

    choose_transport = forms.ChoiceField(
        label='Пътувам с',
        choices=travel_with,
        widget=forms.RadioSelect,
        initial=19
    )

    email = forms.EmailField(
        label='Имейл',
        widget=forms.EmailInput(
            attrs={
                'required': False
            }
        ),
        required=False
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_choose_hike(self):
        chosen_hike = self.cleaned_data.get('choose_hike')

        if chosen_hike not in self.request.path.split('/'):
            self.add_error('choose_hike', 'Моля опитайте отново')

        return chosen_hike

    def clean_choose_transport(self):
        chosen_transport = self.cleaned_data.get('choose_transport')

        if not check_is_digit(chosen_transport) \
                and not -1 < int(chosen_transport) < len(SignUpForHike.TRAVEL_CHOICES.get_all_choices()):
            self.add_error('choose_transport', 'Моля опитайте отново')

        return chosen_transport

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and UserModel.objects.filter(email=email):
            self.add_error('email', 'Потребител с този имейл съшествува')

        return email

    def clean(self):
        keys_to_delete = ['choose_transport', 'first_name', 'last_name', 'phone_number', 'choose_hike', 'email']
        cleaned_data = super().clean()

        if isinstance(self.request.user, UserModel):
            profile = self.get_user_profile(self.request.user.pk)
        else:
            if 'email' in cleaned_data and cleaned_data['email']:
                profile = self.register_profile_with_random_password(
                    email=cleaned_data.get('email'),
                    last_name=cleaned_data.get('last_name'),
                    first_name=cleaned_data.get('first_name'),
                    phone_number=cleaned_data.get('phone_number')
                )
                user_app = UserModel.objects.get(pk=profile.user_id.pk)
                login(self.request, user=user_app)
            else:
                profile = AnonymousAppUser.objects.create(
                    last_name=cleaned_data.get('last_name'),
                    first_name=cleaned_data.get('first_name'),
                    phone_number=cleaned_data.get('phone_number')
                )

        cleaned_data['hike_id'] = Hike.objects.get(pk=cleaned_data.get('choose_hike'))
        cleaned_data['user_type'] = ContentType.objects.get_for_model(profile)
        cleaned_data['user_id'] = profile.pk
        cleaned_data['travel_with'] = self.cleaned_data.get('choose_transport')

        for key in keys_to_delete: del cleaned_data[key]

        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)

        sing_up_for_hike_obj = self.cleaned_data

        if commit:
            SignUpForHike.objects.create(**sing_up_for_hike_obj)

        return obj

    class Meta:
        model = SignUpForHike
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'adults_numbers',
            'children_numbers',
            'choose_hike',
            'choose_transport',
            'email',
        )


class SignedForHikeUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=BaseProfile.FIRST_NAME_MAX_LENGTH,
        label='Име',
        widget=forms.TextInput(attrs={
            'value': '',
        })
    )

    last_name = forms.CharField(
        max_length=BaseProfile.LAST_NAME_MAX_LENGTH,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'value': '',
        })
    )

    phone_number = forms.CharField(
        max_length=BaseProfile.PHONE_NUMBER_MAX_LENGTH,
        label='Телефон',
        widget=forms.TextInput(attrs={
            'value': '',
        })
    )

    def save(self, commit=True):
        obj = super().save(commit=False)
        user = obj.user_object.__class__._default_manager.get(pk=obj.user_id)

        if self.cleaned_data['first_name'] and self.cleaned_data['first_name'] != obj.user_object.first_name:
            user.first_name = self.cleaned_data['first_name']

        if self.cleaned_data['last_name'] and self.cleaned_data['last_name'] != obj.user_object.last_name:
            user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['phone_number'] and self.cleaned_data['phone_number'] != obj.user_object.phone_number:
            user.phone_number = self.cleaned_data['phone_number']

        user.save()

        if commit:
            obj.save()

        return obj

    class Meta:
        model = SignUpForHike
        fields = (
            'hike_id', 'first_name', 'last_name', 'phone_number', 'travel_with', 'adults_numbers', 'children_numbers')
        labels = {
            'hike_id': 'Походи',
            'adults_numbers': 'Брой възрастни',
            'children_numbers': 'Брой деца',
            'travel_with': 'Пъвува с'
        }


class EvaluationBaseForm(forms.Form):
    assessment = forms.ChoiceField(
        label='Оценка',
        widget=forms.RadioSelect(),
        validators=(ValueInRangeValidator(1, 11),),
        choices=[(x, x) for x in range(1, 11)]
    )

    comment = forms.CharField(
        label='Описание',
        widget=forms.Textarea(),
        required=False,
    )


class SiteEvaluationForm(EvaluationBaseForm, forms.ModelForm):
    class Meta:
        model = SiteEvaluation
        fields = '__all__'


class HikeEvaluationForm(EvaluationBaseForm, forms.ModelForm):
    class Meta:
        model = HikeEvaluation
        fields = '__all__'


class SliderCreateForm(PicturesMixin, forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
        error_messages = {
            'hike_id': {
                'unique': _('Слайдър за този поход вече съществува.')
            },
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        folder = f'slider/{obj.hike_id.slug}'
        obj.image = self.upload_picture(
            file=self.cleaned_data['image'].file,
            folder=folder
        )

        if commit:
            obj.save()

        return obj


class SliderEditForm(PicturesMixin, forms.ModelForm):
    image = forms.ImageField(
        label='Снимка',
        widget=forms.FileInput(),
    )

    class Meta:
        model = Slider
        fields = '__all__'
        error_messages = {
            'hike_id': {
                'unique': _('Слайдър за този поход вече съществува.')
            },
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        public_id = self.initial['image'].public_id
        self.delete_pictures(public_id)
        folder = '/'.join(public_id.split('/')[:2])
        obj.image = self.upload_picture(
            file=self.cleaned_data['image'].file,
            folder=folder
        )

        if commit:
            obj.save()

        return obj
