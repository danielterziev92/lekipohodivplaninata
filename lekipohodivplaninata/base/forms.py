from django import forms

from lekipohodivplaninata.base.models import SignUpForHike, TravelWith
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile
from lekipohodivplaninata.users_app.models import UserApp


class SignUpHikeForm(forms.ModelForm):
    hikes = tuple(Hike.objects.all().values_list('id', 'title'))
    travel_with = tuple(TravelWith.objects.all().values_list())

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

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        obj = super().save(commit=False)

        if isinstance(self.user, UserApp):
            profile = BaseProfile.objects.get(pk=self.user.pk)
            SignUpForHike.user_type = profile
            SignUpForHike.user_id = profile.pk

        return obj
