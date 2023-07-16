from django.contrib import admin

from lekipohodivplaninata.base.models import SocialMedia, Settings


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email_for_contact')
