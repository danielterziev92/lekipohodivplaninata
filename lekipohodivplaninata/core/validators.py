from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValueInRangeValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value):
        if int(value) < self.min_value or self.max_value < int(value):
            raise ValidationError(f'Стойността трябва да бъде между {self.min_value} и {self.max_value}')

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.min_value == other.min_value
                and self.max_value == other.max_value
        )


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        max_size_bytes = self.max_size * 1024 * 1024
        if value.size > max_size_bytes:
            value_in_MiB = value.size / 1024 / 1024
            raise ValidationError(f'Файлът ви е {value_in_MiB:.2f} MB. Трябва да бъде под {self.max_size} MB.')

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.max_size == other.max_size
        )
