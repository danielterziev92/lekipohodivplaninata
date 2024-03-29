from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lekipohodivplaninata.users_app'
    verbose_name = 'Потребители'

    def ready(self):
        import lekipohodivplaninata.users_app.signals
