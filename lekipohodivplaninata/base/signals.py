from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata import settings
from lekipohodivplaninata.base.models import SignUpForHike
from lekipohodivplaninata.core.tasks import send_successful_email_signed_for_hike

DOMAIN_NAME = 'lekipohodivplanina.bg'
SENDER = settings.DEFAULT_FROM_EMAIL


@receiver(signal=post_save, sender=SignUpForHike)
def send_email_for_successful_signed_for_hike(instance, created, *args, **kwargs):
    if created:
        send_successful_email_signed_for_hike.delay(instance.hike_id.pk, instance.user_id)
