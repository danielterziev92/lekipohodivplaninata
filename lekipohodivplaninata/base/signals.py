from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata import settings
from lekipohodivplaninata.base.models import SignUpForHike
from lekipohodivplaninata.core.tasks import send_successful_email_signed_for_hike_confirm, \
    send_successful_email_signed_for_hike
from lekipohodivplaninata.users_app.models import AnonymousAppUser

DOMAIN_NAME = 'lekipohodivplanina.bg'
SENDER = settings.DEFAULT_FROM_EMAIL
UserModel = get_user_model()


@receiver(signal=post_save, sender=SignUpForHike)
def send_email_for_successful_signed_for_hike(instance, created, *args, **kwargs):
    if isinstance(instance.user_object, AnonymousAppUser):
        return

    if created:
        return send_successful_email_signed_for_hike.delay(instance.hike_id.pk, instance.user_id)

    return send_successful_email_signed_for_hike_confirm.delay(
        instance.hike_id.pk, instance.user_id, instance.travel_with
    )
