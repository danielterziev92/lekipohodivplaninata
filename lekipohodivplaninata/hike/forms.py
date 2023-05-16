from django import forms
from cloudinary import forms as cloudinary_form

from lekipohodivplaninata.hike.models import Hike, HikeLevel
from lekipohodivplaninata.users_app.models import BaseProfile


class HikeForm(forms.ModelForm):
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

    main_picture = cloudinary_form.CloudinaryFileField(
        label='Освновна снимка',
        options={
            'folder': Hike.PICTURE_DIRECTORY
        }
    )

    class Meta:
        model = Hike
        fields = ('title', 'level', 'event_date', 'duration', 'price', 'main_picture', 'description')


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
