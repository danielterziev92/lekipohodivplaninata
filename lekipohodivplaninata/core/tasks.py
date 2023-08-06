import datetime

from celery import Celery
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from lekipohodivplaninata.hike.models import Hike, HikeAdditionalInfo
from lekipohodivplaninata.users_app.models import BaseProfile

LOGO = settings.LOGO
PROTOCOL = settings.DEFAULT_PROTOCOL
DOMAIN_NAME = settings.SITE_DOMAIN
SENDER = settings.DEFAULT_FROM_EMAIL
UserModel = get_user_model()
app = Celery()


def get_hike(hike_id):
    return Hike.objects.get(pk=hike_id)


def get_hike_additional_info(hike_id):
    return HikeAdditionalInfo.objects.get(hike_id_id=hike_id)


def get_user_profile(user_id):
    return BaseProfile.objects.get(pk=user_id)


def get_signed_for_hike_base_context(hike_id, user_id):
    hike = get_hike(hike_id)
    hike_additional_info = get_hike_additional_info(hike_id)
    user = get_user_profile(user_id)
    return {
        'logo': LOGO,
        'protocol': PROTOCOL,
        'domain': DOMAIN_NAME,
        'hike': hike,
        'additional_info': hike_additional_info,
        'user': user
    }


def get_signed_for_hike_organized_transport_context(hike_id, user_id):
    hike = get_hike(hike_id)
    hike_additional_info = {
        'event_venue': 'гр. Бургас',
        'departure_place': 'Лидл зад автогара Запад',
        'departure_time': '8:00',
    }
    user = get_user_profile(user_id)
    return {
        'logo': LOGO,
        'protocol': PROTOCOL,
        'domain': DOMAIN_NAME,
        'hike': hike,
        'additional_info': hike_additional_info,
        'user': user
    }


@shared_task
def send_successful_registration_user_profile(user_pk, raw_password):
    user = BaseProfile.objects.get(pk=user_pk)

    context = {
        'logo': LOGO,
        'protocol': PROTOCOL,
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
    context = get_signed_for_hike_base_context(hike_id=hike_id, user_id=user_id)

    recipient_list = (context['user'].get_email,)

    message = render_to_string(
        template_name='hike/email-templates/sign-up-for-hike-general.html',
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
def send_successful_email_signed_for_hike_confirm(hike_id, user_id, travel_with):
    if travel_with == 1:
        context = get_signed_for_hike_base_context(hike_id=hike_id, user_id=user_id)
    else:
        context = get_signed_for_hike_organized_transport_context(hike_id=hike_id, user_id=user_id)

    recipient_list = (context['user'].get_email,)

    message = render_to_string(
        template_name='hike/email-templates/sign-up-for-hike-successful-signed.html',
        context=context
    )

    send_mail(
        subject='Потвърждаване на записване за поход',
        message='',
        from_email=SENDER,
        recipient_list=recipient_list,
        html_message=message,
    )


@shared_task
def send_reset_password_user_email(user_id, *args, **kwargs):
    user = BaseProfile.objects.get(pk=user_id)

    context = {
        'logo': LOGO,
        'protocol': PROTOCOL,
        'domain': DOMAIN_NAME,
        'ip_address': kwargs.get('ip_address'),
        'user': user,
        'uid': kwargs.get('uid'),
        'token': kwargs.get('token'),
        'time_remaining': (
                datetime.datetime.now() + datetime.timedelta(hours=settings.PASSWORD_RESET_TIMEOUT))
        .strftime('%d-%m-%Y %H:%M часа')
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


@shared_task
def send_email_for_hike_evaluation_with_slug_to_log_in(**kwargs):
    user = BaseProfile.objects.get(pk=kwargs['user_id'])

    context = {
        'logo': LOGO,
        'protocol': PROTOCOL,
        'domain': DOMAIN_NAME,
        'user': user,
        'slug': kwargs['slug'],
    }

    recipient_list = (user.get_email,)

    message = render_to_string(
        template_name='hike/email-templates/hike-evaluation.html',
        context=context
    )

    send_mail(
        subject='Как ще оцените нашето обслужване?',
        message='',
        from_email=SENDER,
        recipient_list=recipient_list,
        html_message=message,
    )
