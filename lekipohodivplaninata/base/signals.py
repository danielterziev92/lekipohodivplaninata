import datetime

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata import settings
from lekipohodivplaninata.base.models import HikeEvaluation, SignUpForHike
from lekipohodivplaninata.core.tasks import send_email_for_hike_evaluation_with_slug_to_log_in, \
    send_successful_email_signed_for_hike_confirm, send_successful_email_signed_for_hike
from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import AnonymousAppUser

DOMAIN_NAME = settings.SITE_DOMAIN
SENDER = settings.DEFAULT_FROM_EMAIL
UserModel = get_user_model()


@receiver(signal=post_save, sender=SignUpForHike)
def send_email_for_successful_signed_for_hike(instance, created, *args, **kwargs):
    def time_to_seconds(event_date):
        return (event_date - datetime.datetime.today()).total_seconds()

    def get_event_datetime():
        event_time = Hike.objects.get(pk=instance.hike_id.pk).event_date
        future_time = datetime.datetime.combine(event_time, datetime.time(20, 0, 0))
        return time_to_seconds(future_time)

    if isinstance(instance.user_object, AnonymousAppUser):
        return

    if created:
        return send_successful_email_signed_for_hike.delay(instance.hike_id.pk, instance.user_id)

    if cache.get('signed_for_hike_edit_info'):
        cache.delete('signed_for_hike_edit_info')
        return

    hike_eval = HikeEvaluation.objects.get(hike_id=instance.hike_id)
    hike_eval.users.create(user_id=instance.user_object)
    send_mail_datetime = get_event_datetime()
    send_email_for_hike_evaluation_with_slug_to_log_in.apply_async(
        kwargs={
            'user_id': instance.user_id,
            'slug': hike_eval.slug,
        },
        countdown=send_mail_datetime
    )

    return send_successful_email_signed_for_hike_confirm.delay(
        instance.hike_id.pk, instance.user_id, instance.travel_with
    )
