import datetime

from django.core.exceptions import ValidationError


def before_today_validator(value):
    if datetime.date.today() > value:
        raise ValidationError('Датата не може да бъде в миналото')
