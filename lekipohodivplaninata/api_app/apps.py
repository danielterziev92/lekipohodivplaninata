from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lekipohodivplaninata.api_app'

    def ready(self):
        import lekipohodivplaninata.api_app.signals
