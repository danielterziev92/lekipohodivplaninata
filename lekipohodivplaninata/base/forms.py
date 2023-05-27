import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType

from lekipohodivplaninata.base.models import SignUpForHike, TravelWith
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile, AnonymousAppUser, GuideProfile
from lekipohodivplaninata.users_app.models import UserApp

UserModel = get_user_model()


class SignUpHikeForm(forms.ModelForm):
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

    class Meta:
        model = SignUpForHike
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'participants_number', 'choose_hike', 'choose_transport')

    @staticmethod
    def get_user_profile(pk):
        return BaseProfile.objects.get(pk=pk)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if isinstance(self.user, UserModel):
            self.profile = self.get_user_profile(user.pk)

    def clean(self):
        cleaned_data = super().clean()

        if isinstance(self.user, UserModel):
            user = self.get_user_profile(self.user.pk)
        else:
            user = AnonymousAppUser.objects.create(
                first_name=cleaned_data['first_name'],
                last_name=cleaned_data['last_name']
            )

        cleaned_data['hike_id'] = Hike.objects.get(pk=cleaned_data.get('choose_hike'))
        cleaned_data['user_type'] = ContentType.objects.get_for_model(user)
        cleaned_data['user_id'] = user.pk
        cleaned_data['travel_with'] = TravelWith.objects.get(pk=cleaned_data.get('choose_transport', 1))
        cleaned_data['signed_on'] = datetime.datetime.now()

        keys_to_delete = ('choose_transport', 'first_name', 'last_name', 'choose_hike')
        for key in keys_to_delete: del cleaned_data[key]

        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)

        sing_up_for_hike_obj = self.cleaned_data

        if commit:
            SignUpForHike.objects.create(**sing_up_for_hike_obj)

        return obj
