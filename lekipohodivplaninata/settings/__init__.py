import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.environ.get('DEBUG')

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(' ')

from lekipohodivplaninata.settings.django_apps import *
from lekipohodivplaninata.settings.middleware import *

ROOT_URLCONF = 'lekipohodivplaninata.urls'

from lekipohodivplaninata.settings.templates import *

WSGI_APPLICATION = 'lekipohodivplaninata.wsgi.application'

from lekipohodivplaninata.settings.database import *

from lekipohodivplaninata.settings.password_validators import *

from lekipohodivplaninata.settings.common import *

from lekipohodivplaninata.settings.static_and_media_files import *

from lekipohodivplaninata.settings.emails import *

from lekipohodivplaninata.settings.celery import *

from lekipohodivplaninata.settings.cloudinary import *

from lekipohodivplaninata.settings.logging import *
