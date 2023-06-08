import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from lekipohodivplaninata.hike.models import Hike, HikeAdditionalInfo
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


@shared_task
def send_successful_email_signed_for_hike(hike_id, user_id):
    hike = Hike.objects.get(pk=hike_id)
    hike_additional_info = HikeAdditionalInfo.objects.get(hike_id_id=hike_id)
    user = BaseProfile.objects.get(pk=user_id)

    context = {
        'domain': DOMAIN_NAME,
        'hike': hike,
        'additional_info': hike_additional_info,
        'user': user
    }

    recipient_list = (user.get_email,)

    message = render_to_string(
        template_name='hike/email-templates/sign-up-for-hike.html',
        context=context
    )

    send_mail(
        subject='Успешно записване за поход',
        message='',
        from_email=SENDER,
        recipient_list=recipient_list,
        html_message=message,
    )


@shared_task
def send_reset_password_user_email(user_id, *args, **kwargs):
    user = BaseProfile.objects.get(pk=user_id)

    context = {
        'domain': DOMAIN_NAME,
        'ip_address': kwargs.get('ip_address'),
        'user': user,
        'uid': kwargs.get('uid'),
        'token': kwargs.get('token'),
        'protocol': kwargs.get('protocol'),
        'time_remaining': (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%m-%d-%Y %H:%M часа')
    }

    recipient_list = (user.get_email,)

    message = render_to_string(
        template_name='users/email-templates/reset-password.html',
        context=context
    )

    send_mail(
        subject='Забравена парола',
        message='',
        from_email=SENDER,
        recipient_list=recipient_list,
        html_message=message,
    )
