import datetime

from django.core.exceptions import ValidationError


def validate_before_today(value):
    if datetime.date.today() > value:
        raise ValidationError('Датата не може в миналото.')
