import datetime

from django import template
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.hike.models import Hike

register = template.Library()


@register.inclusion_tag(
    'hike/templates/all-recorded-action-buttons.html',
    name='all-recorded-actions',
    takes_context=True
)
def get_all_recorded_action_buttons(context, *args, **kwargs):
    context['event_impend'] = True
    pk, slug, _ = context.request.path[1:-1].split('/')
    hike_event_date = Hike.objects.get(pk=pk, slug=slug).event_date

    if hike_event_date - datetime.timedelta(days=1) < datetime.date.today():
        context['event_impend'] = False

    return context
