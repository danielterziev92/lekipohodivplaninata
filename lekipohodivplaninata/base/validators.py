from django.core.exceptions import ValidationError


def number_between_one_and_ten(value):
    if not 0 < value < 11:
        raise ValidationError('Трябва да избереме оценка от 1 до 10')
