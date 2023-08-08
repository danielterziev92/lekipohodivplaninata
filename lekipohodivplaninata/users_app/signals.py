from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata.core.tasks import send_successful_registration_user_profile
from lekipohodivplaninata.users_app.models import BaseProfile

UserModel = get_user_model()


@receiver(signal=post_save, sender=BaseProfile)
def send_successful_email_for_create_profile_user(instance, created, *args, **kwargs):
    if not created:
        return

    raw_password = cache.get('raw_password')

    if raw_password:
        cache.delete('raw_password')
        send_successful_registration_user_profile.delay(user_pk=instance.pk, raw_password=raw_password)
