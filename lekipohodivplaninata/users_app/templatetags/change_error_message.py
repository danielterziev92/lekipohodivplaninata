from django import template

register = template.Library()


@register.simple_tag(name='change_error_message')
def get_message_and_return_custom(text):
    errors = {
        'The password is too similar to the Email.': 'Паролата ви е много подобна с имейла.',
        'This password is too common.': 'Паролата ви е твърде лесна.',
        'This password is entirely numeric.': 'Паролата ви не трябва да съдържа само цифри.',
        'Enter a valid email address.': 'Невалиден имейл.'
    }

    dynamic_errors = {
        'This password is too short. It must contain at least':
            'Паролата ви е твърде къса. Трябва да съдържа най-малко 8 символа',
    }

    for error in dynamic_errors.keys():
        if text.startswith(error):
            return dynamic_errors[error]

    if text in errors.keys():
        return errors[text]

    return text
