from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

register = template.Library()
UserModel = get_user_model()


@register.inclusion_tag('hike/templates/sign-for-hike-base.html', name='sign_for_hike', takes_context=True)
def get_user_first_name_sign_for_hike(context):
    user_data = {
        'first_name': '',
        'last_name': '',
        'phone_number': '',
        'adults_numbers': '',
        'children_numbers': '',
        'choose_transport': '',
        'email': '',
        'register_user': False,
    }

    if isinstance(context.request.user, UserModel):
        user_data = context.request.user.baseprofile

    if isinstance(context.request.user, AnonymousUser) and context.request.POST:
        user_data = context.request.POST

    for key in user_data.keys():
        context[key] = user_data[key]

    if 'email' in context.request.POST and context.request.POST['email']:
        context['register_user'] = True

    return context
