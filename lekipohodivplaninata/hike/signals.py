from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from lekipohodivplaninata.base.models import HikeEvaluation
from lekipohodivplaninata.core.mixins import CommonMixin
from lekipohodivplaninata.hike.models import Hike


@receiver(signal=post_save, sender=Hike)
def create_hike_evaluation_record(instance, created, *args, **kwargs):
    def create_slug():
        return CommonMixin.generate_random_string(HikeEvaluation.SLUG_LENGTH)

    def create_object_to_hike_evaluation():
        slug = create_slug()
        try:
            HikeEvaluation.objects.get(slug=slug)
            return create_object_to_hike_evaluation()
        except ObjectDoesNotExist:
            return HikeEvaluation.objects.create(slug=slug, hike_id=instance)

    if not created:
        return

    create_object_to_hike_evaluation()
    return
