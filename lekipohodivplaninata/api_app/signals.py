from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata.api_app.models import Subscribe
from lekipohodivplaninata.core.tasks import send_email_to_subscriber


@receiver(post_save, sender=Subscribe)
def send_email_when_user_subscribe(sender, instance, created, **kwargs):
    if created:
        send_email_to_subscriber.delay(email=instance.email)
        return
