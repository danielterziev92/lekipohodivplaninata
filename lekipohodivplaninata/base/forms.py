from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

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
    )

    class Meta:
        model = SignUpForHike
        fields = ('first_name', 'last_name', 'participants_number', 'choose_hike', 'choose_transport')

    @staticmethod
    def get_user_profile(user_model):
        return BaseProfile.objects.get(pk=user_model.pk)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if isinstance(self.user, UserModel):
            user = self.get_user_profile(self.user)
            self.fields['first_name'].widget.attrs['value'] = user.first_name
            self.fields['last_name'].widget.attrs['value'] = user.last_name

    def save(self, commit=True):
        obj = super().save(commit=False)

        if isinstance(self.user, UserApp):
            user = BaseProfile.objects.get(pk=self.user.pk)
            SignUpForHike.user_type = user
            SignUpForHike.user_id = user.pk

        if isinstance(self.user, AnonymousUser):
            user = AnonymousAppUser.objects.create(first_name='', last_name='')

        return obj
