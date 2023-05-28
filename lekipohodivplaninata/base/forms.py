import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.contenttypes.models import ContentType

from lekipohodivplaninata.base.models import SignUpForHike, TravelWith, SiteEvaluation
from lekipohodivplaninata.core.mixins import UserDataMixin
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile, AnonymousAppUser

UserModel = get_user_model()


class SignUpHikeForm(UserDataMixin, forms.ModelForm):
    hikes = tuple(Hike.objects.all().values_list('id', 'title'))
    travel_with = tuple(TravelWith.objects.all().values_list())

    first_name = forms.CharField(
        label='Име',
        widget=forms.TextInput(
            attrs={
                'id': 'first-name',
                'value': '',
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

    participants_number = forms.IntegerField(
        label='Брой участници',
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

    create_registration = forms.BooleanField(
        label='Създай ми регистрация',
        widget=forms.CheckboxInput(
            attrs={
                'checked': False,
                'required': False,
            }
        )
    )

    email = forms.EmailField(
        label='Имейл',
        widget=forms.EmailInput(
            attrs={
                'required': False
            }
        )
    )

    class Meta:
        model = SignUpForHike
        fields = (
            'first_name',
            'last_name',
            'participants_number',
            'choose_hike',
            'choose_transport',
            'create_registration',
            'email',
        )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        keys_to_delete = ['choose_transport', 'first_name', 'last_name', 'choose_hike']
        cleaned_data = super().clean()

        if isinstance(self.request.user, UserModel):
            user = self.get_user_profile(self.request.user.pk)
        else:
            if cleaned_data['email']:
                user = self.register_base_user(
                    email=cleaned_data['email'],
                    first_name=cleaned_data['first_name'],
                    last_name=cleaned_data['last_name'],
                )
                login(self.request, user=user)
                keys_to_delete.append('email')
            else:
                user = AnonymousAppUser.objects.create(
                    first_name=cleaned_data['first_name'],
                    last_name=cleaned_data['last_name']
                )

        cleaned_data['hike_id'] = Hike.objects.get(pk=cleaned_data.get('choose_hike'))
        cleaned_data['user_type'] = ContentType.objects.get_for_model(user)
        cleaned_data['user_id'] = user.pk
        cleaned_data['travel_with'] = TravelWith.objects.get(pk=cleaned_data.get('choose_transport'))

        for key in keys_to_delete: del cleaned_data[key]

        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)

        sing_up_for_hike_obj = self.cleaned_data

        if commit:
            SignUpForHike.objects.create(**sing_up_for_hike_obj)

        return obj


class SiteEvaluationForm(forms.ModelForm):
    assessment = forms.ChoiceField(
        label='Оценка',
        widget=forms.RadioSelect,
        choices=[(x, x) for x in range(1, 11)]
    )

    class Meta:
        model = SiteEvaluation
        fields = '__all__'
