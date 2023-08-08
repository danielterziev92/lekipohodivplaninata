import os

from django.core.wsgi import get_wsgi_application

from lekipohodivplaninata.core.check_connections import CheckConnectionsCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lekipohodivplaninata.settings')

CheckConnectionsCommand().handle()

application = get_wsgi_application()
