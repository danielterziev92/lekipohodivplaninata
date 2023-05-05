import re

from django import template

register = template.Library()


def get_pure_text(text):
    expression = r'(<li>(?P<text>(.*?))<\/li>)'
    result = []
    matches = re.finditer(expression, text)

    for match in matches:
        result.append(match.group(text))

    return result


@register.simple_tag(name='change_help_text')
def get_help_text_and_return_custom_text(help_text):
    new_help_text = []
    messages = {
        'Your password can’t be too similar to your other personal information.': '',
        'Your password must contain at least 8 characters.': '',
        'Your password can’t be a commonly used password.': '',
        'Your password can’t be entirely numeric.': '',
    }

    return new_help_text

# users/password-reset/MzU/bnqzo3-23deac8347816c77d8ad2a009d1f05b8
