import datetime

from django.core.exceptions import ValidationError


def before_today_validator(value):
    if datetime.date.today() > value:
        raise ValidationError('Датата не може да бъде в миналото')

# class BeforeTodayValidator:
#     def __call__(self, value):
#         print(value)
#         # if datetime.date.today() > args:
#         #     raise ValidationError(f'Датата не може да бъде в миналото')
#
#     def __eq__(self, other):
#         return isinstance(other, self.__class__)
