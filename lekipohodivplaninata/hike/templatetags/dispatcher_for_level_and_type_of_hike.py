from django import template
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

register = template.Library()

from lekipohodivplaninata.hike.models import HikeLevel, HikeType


@register.inclusion_tag('hike/templates/list-type-or-level.html', name='dispatcher-hike-or-level', takes_context=True)
def sign_me_for_hike_button(context, *args, **kwargs):
    if issubclass(context.dicts[3]['object_list'].model, HikeLevel):
        context['form_title'] = 'Нива на поход'
        context['obj_edit_url'] = _('hike level update')
        context['obj_delete_url'] = _('hike level delete')
        context['button_action_url'] = _('hike level create')
    else:
        context['form_title'] = 'Типове на трудност'
        context['obj_edit_url'] = _('hike type update')
        context['obj_delete_url'] = _('hike type delete')
        context['button_action_url'] = _('hike type create')

    return context


@register.simple_tag(name='type_or_level_form_url', takes_context=True)
def create_or_update_type_or_level_form_url(context, *args, **kwargs):
    main, action, type, *id = get_params_from_url(context.request.path)

    if id:
        return reverse_lazy(f'{main} {type} {action}', kwargs={'pk': int(id[0])})

    return reverse_lazy(f'{main} {type} {action}')


@register.simple_tag(name='type_or_level_form_title', takes_context=True)
def create_or_update_type_or_level_form_title(context, *args, **kwargs):
    title = ''
    _, action, type, *params = get_params_from_url(context.request.path)
    if action == 'create':
        title += 'Добави '
    else:
        title += 'Редактиране'

    if type == 'level':
        title += 'ниво на похода'
    else:
        title += 'тип на трудност'

    return title


@register.simple_tag(name='type_or_level_button_text', takes_context=True)
def create_or_update_type_or_level_button_text(context, *args, **kwargs):
    main, action, type, *id = get_params_from_url(context.request.path)

    if action == 'create':
        return 'Добави'

    return 'Редакция'


def get_params_from_url(url):
    return url[1:-1].split('/')
