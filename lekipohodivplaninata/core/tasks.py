from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

DOMAIN_NAME = 'lekipohodivplanina.bg'
SENDER = settings.EMAIL_HOST_USER
UserModel = get_user_model()


@shared_task
def send_successful_registration_app_user_with_random_password(user_pk, raw_password, profile_pk):
    user = UserModel.objects.get(pk=user_pk)
    recipient_list = (user.email,)
    message = f'This is your raw_password: {raw_password}'

    send_mail(
        subject=DOMAIN_NAME,
        message=message,
        from_email=SENDER,
        recipient_list=recipient_list,
        html_message='',
    )
