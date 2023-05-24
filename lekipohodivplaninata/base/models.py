from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from lekipohodivplaninata.hike.models import Hike
from lekipohodivplaninata.users_app.models import BaseProfile

BaseUserModel = BaseProfile
HikeModel = Hike


class TravelWith(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )


class SignUpForHike(models.Model):
    hike_id = models.ForeignKey(
        HikeModel,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    user_type = models.ForeignKey(
        ContentType,
        on_delete=models.RESTRICT
    )

    user_id = models.PositiveIntegerField()

    user_object = GenericForeignKey('user_type', 'user_id')

    travel_with = models.ForeignKey(
        TravelWith,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    participants_number = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    signed_on = models.DateTimeField(
        auto_now_add=True,
    )
