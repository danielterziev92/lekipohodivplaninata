import os
from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-xi@15#i77*o9+_uds9024c^pir$si%=)d!19h=$m1h*n46b#02'

DEBUG = True

ALLOWED_HOSTS = ['*']

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

PROJECT_APPS = (
    'lekipohodivplaninata.users_app.apps.UsersAppConfig',
    'lekipohodivplaninata.base.apps.BaseConfig',
    'lekipohodivplaninata.hike.apps.HikeConfig',
)

THIRD_PARTY_APP = ()

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APP

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lekipohodivplaninata.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lekipohodivplaninata.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lekipohodi',
        'USER': 'postgres',
        'PASSWORD': '1123QwER',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "templates/static/",
]

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'templates/media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users_app.UserApp'

LOGIN_URL = reverse_lazy('sign in user')

LOGOUT_REDIRECT_URL = reverse_lazy('index')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'localhost'

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_PORT = 25

# EMAIL_USE_TLS = True

EMAIL_SUBJECT_PREFIX = 'LekiPohodiVPlaninata.BG'

# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': [],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }
