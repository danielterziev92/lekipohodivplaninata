from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from lekipohodivplaninata.users_app.models import BaseProfile

DOMAIN_NAME = 'lekipohodivplaninata.bg'
SENDER = settings.DEFAULT_FROM_EMAIL
UserModel = get_user_model()


@shared_task
def send_successful_registration_user_profile(user_pk, raw_password):
    user = BaseProfile.objects.get(pk=user_pk)

    context = {
        'domain': DOMAIN_NAME,
        'user': user,
    }

    if raw_password:
        context['password'] = raw_password

    recipient_list = (user.get_email,)

    message = render_to_string(
        template_name='users/email-templates/user-sign-up.html',
        context=context)

    send_mail(
        subject='Регистрация',
        message='',
        from_email=SENDER,
        recipient_list=recipient_list,
        html_message=message,
    )
