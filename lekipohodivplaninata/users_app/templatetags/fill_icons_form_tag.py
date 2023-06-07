from django import template

register = template.Library()


@register.simple_tag(name='form_icons')
def get_icon_for_form(label_id):
    icons_class = {
        'id_email': 'fas fa-envelope',
        'password_1': 'fas fa-lock',
        'password_2': 'fas fa-lock',
        'id_password': 'fas fa-lock',
        'id_first_name': 'fa-regular fa-user',
        'id_last_name': 'fa-regular fa-user',
        'id_avatar': 'fa-solid fa-link',
        'id_certificate': 'fa-solid fa-link',
        'id_date_of_birth': 'fa-regular fa-calendar-days',
        'id_description': 'fa-solid fa-text-height',
        'id_phone_number': 'fa-solid fa-phone',
    }

    return icons_class.get(label_id, 'fa-solid fa-question')
