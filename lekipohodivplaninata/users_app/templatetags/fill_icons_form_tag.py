from django import template

register = template.Library()


@register.simple_tag(name='form_icons')
def get_icon_for_form(label_id):
    icons_class = {
        'id_email': 'fas fa-envelope',
        'id_password': 'fas fa-lock',
        'id_password1': 'fas fa-lock',
        'id_password2': 'fas fa-lock',
        'id_first_name': 'fa-regular fa-user',
        'id_last_name': 'fa-regular fa-user',
    }

    try:
        return icons_class[label_id]
    except KeyError:
        return 'fa-solid fa-question'
