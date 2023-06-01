from django import forms
from django.core.cache import cache
from django.forms import FileInput

from lekipohodivplaninata.core.mixins import HikeCreateFormMixin, HikeUpdateFormMixin, PicturesMixin
from lekipohodivplaninata.hike.models import Hike, HikeLevel, HikeMorePicture
from lekipohodivplaninata.hike.models import HikeAdditionalInfo
from lekipohodivplaninata.hike.models import HikeType
from lekipohodivplaninata.users_app.models import BaseProfile


class HikeForm(PicturesMixin, forms.ModelForm):
    title = forms.CharField(
        max_length=Hike.TITLE_MAX_LENGTH,
        label='Заглавие',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Въведете заглавие',
            }
        ),
    )

    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(
            attrs={
                'cols': 30,
                'rows': 10,
                'placeholder': 'Въведете описание на похода',
            }
        )
    )

    type = forms.ModelChoiceField(
        label='Ниво на трудност',
        empty_label='Изберете ниво',
        queryset=HikeType.objects.all()
    )

    level = forms.ModelChoiceField(
        label='Ниво на похода',
        empty_label='Изберете ниво',
        queryset=HikeLevel.objects.all()
    )

    event_date = forms.DateField(
        label='Дата на събитието',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    duration = forms.CharField(
        label='Продължителност',
        widget=forms.TextInput(),
    )

    price = forms.DecimalField(
        label='Цена на човек',
        decimal_places=2,
    )


class HikeCreateForm(HikeCreateFormMixin, HikeForm):
    main_picture = forms.ImageField(
        label='Освновна снимка',
        widget=FileInput,
    )

    event_venue = forms.CharField(
        label='Място на събитието',
        max_length=HikeAdditionalInfo.EVENT_VENUE_MAX_LENGTH,
        widget=forms.TextInput(),
    )

    departure_time = forms.TimeField(
        label='Час на тръгване',
        widget=forms.TimeInput(),
    )

    departure_place_value = forms.CharField(
        label='Място на тръгване',
        max_length=HikeAdditionalInfo.DEPARTURE_PLACE_MAX_LENGTH,
        widget=forms.TextInput(),
    )

    class Meta:
        model = Hike
        fields = (
            'title', 'type', 'level', 'event_date', 'duration', 'price', 'main_picture', 'description',
            'event_venue', 'departure_place_value', 'departure_time')


class HikeUpdateForm(HikeUpdateFormMixin, HikeForm):
    new_main_picture = forms.ImageField(
        label='Освновна снимка',
        widget=FileInput,
        required=False,
    )

    event_venue = forms.CharField(
        label='Място на събитието',
        max_length=HikeAdditionalInfo.EVENT_VENUE_MAX_LENGTH,
        widget=forms.TextInput(
            attrs={
                'value': cache.get('event_venue', '')
            }
        ),
    )

    departure_time = forms.TimeField(
        label='Час на тръгване',
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'value': cache.get('departure_time', '')
            }
        ),
    )

    departure_place_value = forms.CharField(
        label='Място на тръгване',
        max_length=HikeAdditionalInfo.DEPARTURE_PLACE_MAX_LENGTH,
        widget=forms.TextInput(
            attrs={
                'value': cache.get('departure_place', '')
            }
        ),
    )

    class Meta:
        model = Hike
        fields = ('title', 'level', 'type', 'event_date', 'duration', 'price', 'new_main_picture', 'description',
                  'event_venue', 'departure_place_value', 'departure_time')


class HikeMorePictureUploadForm(forms.ModelForm):
    pk = forms.HiddenInput()

    picture = forms.ImageField(
        label='Снимка',
        widget=FileInput,
        required=False,
    )

    class Meta:
        model = HikeMorePicture
        fields = ('picture',)


class SignUpForHikeForm(forms.Form):
    TRAVEL_WITH = (
        ('organized-transport', 'Организиран транспорт'),
        ('personal-transport', 'Собствен Транспорт'),
    )

    first_name = forms.CharField(
        max_length=BaseProfile.FIRST_NAME_MAX_LENGTH,
        label='Име',
        widget=forms.TextInput()
    )

    last_name = forms.CharField(
        max_length=BaseProfile.LAST_NAME_MAX_LENGTH,
        label='Фамилия',
        widget=forms.TextInput()
    )

    participants_count = forms.IntegerField(
        label='Брой участници',
    )

    hikes = forms.ChoiceField(
        label='Избери поход',
        choices=(
            [(hike.pk, hike.title) for hike in Hike.objects.all()]
        )
    )

    travel_with = forms.ChoiceField(
        label='Ще пътувам с',
        choices=TRAVEL_WITH,
    )
