import os

from django.core.asgi import get_asgi_application

from lekipohodivplaninata.core.check_connections import CheckConnectionsCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lekipohodivplaninata.settings')

CheckConnectionsCommand().handle()

application = get_asgi_application()
