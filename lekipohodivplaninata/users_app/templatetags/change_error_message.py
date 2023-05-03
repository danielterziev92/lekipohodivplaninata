from django import template

register = template.Library()


@register.simple_tag(name='change_error_message')
def get_message_and_return_custom(text):
    errors = {
        'The password is too similar to the Email.': 'Паролата ви е много подобна с имейла.'
    }

    if text in errors.keys():
        return errors[text]

    return text
