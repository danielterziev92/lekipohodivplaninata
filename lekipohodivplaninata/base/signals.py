import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata import settings
from lekipohodivplaninata.base.models import HikeEvaluation, SignUpForHike
from lekipohodivplaninata.base.models import HikeEvaluationUsers
from lekipohodivplaninata.core.mixins import CommonMixin
from lekipohodivplaninata.core.tasks import send_email_for_hike_evaluation_with_slug_to_log_in, \
    send_successful_email_signed_for_hike_confirm, send_successful_email_signed_for_hike
from lekipohodivplaninata.users_app.models import AnonymousAppUser

DOMAIN_NAME = 'lekipohodivplanina.bg'
SENDER = settings.DEFAULT_FROM_EMAIL
UserModel = get_user_model()


@receiver(signal=post_save, sender=SignUpForHike)
def send_email_for_successful_signed_for_hike(instance, created, *args, **kwargs):
    def create_slug():
        return CommonMixin.generate_random_string(HikeEvaluation.SLUG_LENGTH)

    def create_object_to_hike_evaluation():
        slug = create_slug()
        try:
            HikeEvaluation.objects.get(slug=slug)
            return create_object_to_hike_evaluation()
        except ObjectDoesNotExist:
            return HikeEvaluation.objects.create(slug=slug, hike_id=instance.hike_id)

    if isinstance(instance.user_object, AnonymousAppUser):
        return

    if created:
        create_object_to_hike_evaluation()
        return send_successful_email_signed_for_hike.delay(instance.hike_id.pk, instance.user_id)

    HikeEvaluation.objects.get(hike_id=instance.hike_id).users.create(user_id=instance.user_id)
    return send_successful_email_signed_for_hike_confirm.delay(
        instance.hike_id.pk, instance.user_id, instance.travel_with
    )


@receiver(signal=post_save, sender=HikeEvaluation)
def send_mail_for_hike_evaluation(instance, created, *args, **kwargs):
    if created:
        return

    slug = instance.slug

    send_mail_delay = datetime.datetime.now() + datetime.timedelta(minutes=1)
    send_email_for_hike_evaluation_with_slug_to_log_in.apply_async(eta=send_mail_delay)
