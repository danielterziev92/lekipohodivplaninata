from lekipohodivplaninata.base.models import Settings


def get_contacts(request):
    settings = Settings.objects.all().first()

    return {
        'email': settings.email_for_contact,
        'phone_number': settings.phone_number,
        'social_media': settings.social_media
    }
