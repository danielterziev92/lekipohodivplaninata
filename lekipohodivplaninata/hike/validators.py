import datetime

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class BeforeTodayValidator:
    def __call__(self, value):
        if datetime.date.today() > value:
            raise ValidationError(f'Датата не може да бъде в миналото')

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
        )
