import datetime

from django import template

register = template.Library()


@register.simple_tag(name='sign_me_hike_button')
def sign_me_for_hike_button(event):
    if event > datetime.date.today() - datetime.timedelta(days=1):
        return True

    return False
