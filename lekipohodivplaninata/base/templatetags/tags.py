import datetime

from django import template
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.hike.models import Hike

register = template.Library()
DOMAIN_NAME = 'lekipohodivplanina.bg'


@register.inclusion_tag('hike/templates/all-recorded-action-buttons.html', name='all-recorded-actions', )
def get_all_recorded_action_buttons(obj):
    context = {
        'event_impend': True,
        'hike': Hike.objects.get(pk=obj.hike_id_id),
        'pk': obj.pk,
    }

    hike_event_date = context['hike'].event_date

    if hike_event_date - datetime.timedelta(days=1) < datetime.date.today():
        context['event_impend'] = False

    return context
