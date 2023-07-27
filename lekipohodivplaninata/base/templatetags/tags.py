import datetime

from django import template
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.base.models import SignUpForHike, Hike, SiteEvaluation

register = template.Library()
DOMAIN_NAME = 'lekipohodivplanina.bg'


def get_total_count(objects):
    result = 0
    for obj in objects:
        result += obj.adults_numbers + obj.children_numbers

    return result


@register.inclusion_tag('hike/templates/all-recorded-action-buttons.html', name='all-recorded-actions', )
def get_all_recorded_action_buttons(obj):
    context = {
        'event_impend': True,
        'hike': Hike.objects.get(pk=obj.hike_id_id),
        'pk': obj.pk,
        'is_confirmed': True if obj.is_confirmed is None else False,
        'is_presence': True if obj.is_presence is None else False,
    }

    hike_event_date = context['hike'].event_date

    if hike_event_date - datetime.timedelta(days=1) < datetime.date.today():
        context['event_impend'] = False

    return context


@register.simple_tag(name='total-travel-with-organized-transport')
def get_all_travel_with_organized_transport(hike_pk):
    persons = SignUpForHike.objects.all().filter(hike_id=hike_pk).filter(travel_with=0)
    return get_total_count(persons)


@register.simple_tag(name='total-adults-with-organized-transport')
def get_all_travel_with_organized_transport(hike_pk):
    objects = SignUpForHike.objects.all().filter(hike_id=hike_pk).filter(travel_with=0) \
        .filter(adults_numbers__gt=0)
    return sum(obj.adults_numbers for obj in objects)


@register.simple_tag(name='total-children-with-organized-transport')
def get_all_travel_with_organized_transport(hike_pk):
    objects = SignUpForHike.objects.all().filter(hike_id=hike_pk).filter(travel_with=0) \
        .filter(children_numbers__gt=0)
    return sum(obj.children_numbers for obj in objects)


@register.simple_tag(name='total-travel-with-own-transport')
def get_all_travel_with_organized_transport(hike_pk):
    persons = SignUpForHike.objects.all().filter(hike_id=hike_pk).filter(travel_with=1)
    return get_total_count(persons)


@register.simple_tag(name='total-count-for-hike')
def get_all_travel_with_organized_transport(a, b):
    return a + b


@register.simple_tag(name='show_error_message')
def get_error_message_for_field(errors: dict):
    result = []
    for field, values in errors.items():
        if field == '__all__':
            continue

        result.extend([value for value in values])
    return result


@register.simple_tag(name='average_site_evaluation')
def get_average_site_evaluation():
    site_evaluations = SiteEvaluation.objects.all()
    site_evaluations_grades = sum([evaluation.assessment for evaluation in site_evaluations])
    site_evaluations_count = site_evaluations.count()
    result = site_evaluations_grades / site_evaluations_count

    return f'{result:.2f}'
