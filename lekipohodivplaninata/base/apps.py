from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lekipohodivplaninata.base'

    def ready(self):
        import lekipohodivplaninata.base.signals
