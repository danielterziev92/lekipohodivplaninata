import re

from django.core import validators
from django.utils.translation import gettext_lazy as _


class ContainUppercasePasswordValidator:
    def __init__(self):
        self.pattern = "[A-ZА-Я]"

    def validate(self, password, user):
        matches = re.findall(self.pattern, password)
        if not len(matches):
            raise validators.ValidationError(
                _('Паролата ви трябва да съдържа поне една главна буква'), code='invalid')

    def get_help_text(self):
        return ''


class ContainLowercasePasswordValidator:
    def __init__(self):
        self.pattern = "[a-zа-я]"

    def validate(self, password, user):
        matches = re.findall(self.pattern, password)
        if not len(matches):
            raise validators.ValidationError(
                _('Паролата ви трябва да съдържа поне една малка буква'), code='invalid')

    def get_help_text(self):
        return ''
