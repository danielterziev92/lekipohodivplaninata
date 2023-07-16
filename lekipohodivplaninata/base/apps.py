from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lekipohodivplaninata.base'
    verbose_name = 'Основни настройки'

    def ready(self):
        import lekipohodivplaninata.base.signals
