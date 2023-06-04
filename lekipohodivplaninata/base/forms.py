from django import forms
from django.contrib.auth import get_user_model, login
from django.contrib.contenttypes.models import ContentType

from lekipohodivplaninata.base.models import SignUpForHike, SiteEvaluation
from lekipohodivplaninata.core.mixins import UserDataMixin
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import AnonymousAppUser

UserModel = get_user_model()


class SignUpHikeForm(UserDataMixin, forms.ModelForm):
    hikes = tuple(Hike.objects.all().values_list('id', 'title'))
    travel_with = tuple(SignUpForHike.TRAVEL_CHOICES.get_all_choices())

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
            'email',
        )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        keys_to_delete = ['choose_transport', 'first_name', 'last_name', 'choose_hike']
        cleaned_data = super().clean()

        if isinstance(self.request.user, UserModel):
            profile = self.get_user_profile(self.request.user.pk)
        else:
            if cleaned_data['email']:
                profile = self.register_profile_with_random_password(
                    last_name=cleaned_data['last_name'],
                    email=cleaned_data['email'],
                    first_name=cleaned_data['first_name'],
                )
                user_app = UserModel.objects.get(pk=profile.user_id.pk)
                login(self.request, user=user_app)
                keys_to_delete.append('email')
            else:
                profile = AnonymousAppUser.objects.create(
                    first_name=cleaned_data['first_name'],
                    last_name=cleaned_data['last_name']
                )

        cleaned_data['hike_id'] = Hike.objects.get(pk=cleaned_data.get('choose_hike'))
        cleaned_data['user_type'] = ContentType.objects.get_for_model(profile)
        cleaned_data['user_id'] = profile.pk
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
