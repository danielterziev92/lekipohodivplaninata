import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "templates/static/",
]

STATIC_ROOT = '/tmp/lekipohodivplaninata/staticfiles/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'templates/media')
