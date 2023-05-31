from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata import settings
from lekipohodivplaninata.core.tasks import send_successful_registration_user_profile
from lekipohodivplaninata.users_app.models import BaseProfile

DOMAIN_NAME = 'lekipohodivplanina.bg'
SENDER = settings.DEFAULT_FROM_EMAIL
UserModel = get_user_model()


@receiver(signal=post_save, sender=BaseProfile)
def send_successful_email_for_create_profile_user(instance, created, *args, **kwargs):
    raw_password = cache.get('raw_password')

    send_successful_registration_user_profile.delay(user_pk=instance.pk, raw_password=raw_password)
