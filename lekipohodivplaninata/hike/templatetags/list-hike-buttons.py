import datetime

from django import template
from django.contrib.auth import get_user_model

register = template.Library()

UserModel = get_user_model()


@register.inclusion_tag('hike/templates/list-hike-buttons.html', name='list_hike_buttons')
def list_hike_buttons(user, hike):
    context = {
        'sign_me_hike_button': False,
        'edit_hike_button': False,
        'hike': hike,
    }

    if isinstance(user, UserModel) and user.is_staff:
        context['edit_hike_button'] = True

        return context

    if hike.event_date > datetime.date.today() - datetime.timedelta(days=1):
        context['sign_me_hike_button'] = True

    return context
