from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata import settings
from lekipohodivplaninata.base.models import SignUpForHike
from lekipohodivplaninata.core.tasks import send_successful_email_signed_for_hike_with_own_transport, \
    send_successful_email_signed_for_hike_with_organize_transport
from lekipohodivplaninata.users_app.models import AnonymousAppUser

DOMAIN_NAME = 'lekipohodivplanina.bg'
SENDER = settings.DEFAULT_FROM_EMAIL
UserModel = get_user_model()


@receiver(signal=post_save, sender=SignUpForHike)
def send_email_for_successful_signed_for_hike(instance, created, *args, **kwargs):
    instance_choices = {
        '0': send_successful_email_signed_for_hike_with_own_transport,
        '1': send_successful_email_signed_for_hike_with_organize_transport,
    }

    if created:
        if isinstance(instance.user_object, AnonymousAppUser):
            return

        # if instance.
        return instance_choices[instance.travel_with].delay(instance.hike_id.pk, instance.user_id)
