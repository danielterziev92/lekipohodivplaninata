import os
import datetime
import cloudinary

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from pathlib import Path
from decouple import config as de_config

import lekipohodivplaninata.users_app.validators

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_PROTOCOL = de_config('SITE_PROTOCOL')
SITE_DOMAIN = de_config('SITE_DOMAIN')
LOGO = de_config('SITE_LOGO')

SECRET_KEY = de_config('SECRET_KEY')

DEBUG = de_config('DEBUG')

ALLOWED_HOSTS = de_config('ALLOWED_HOSTS').split(' ')

CSRF_TRUSTED_ORIGINS = [f'https://{x}' for x in ALLOWED_HOSTS]

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
    'lekipohodivplaninata.hike.apps.HikeConfig',
    'lekipohodivplaninata.base.apps.BaseConfig',
)

THIRD_PARTY_APP = (
    'rest_framework',
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APP

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# SOCIAL_AUTH_FACEBOOK_KEY = de_config('FACEBOOK_APP_ID')
# SOCIAL_AUTH_FACEBOOK_SECRET = de_config('FACEBOOK_APP_SECRET')
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = de_config('GOOGLE_CLIENT_ID')
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = de_config('GOOGLE_CLIENT_SECRET')

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
                'lekipohodivplaninata.core.context_processors.get_contacts',
            ],
        },
    },
]

WSGI_APPLICATION = 'lekipohodivplaninata.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': de_config('DB_ENGINE'),
        'NAME': de_config('DB_NAME'),
        'USER': de_config('DB_USER'),
        'PASSWORD': de_config('DB_PASSWORD'),
        'HOST': de_config('DB_HOST'),
        'PORT': de_config('DB_PORT'),
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
    {
        'NAME': 'lekipohodivplaninata.users_app.validators.ContainUppercasePasswordValidator',
    },
    {
        'NAME': 'lekipohodivplaninata.users_app.validators.ContainLowercasePasswordValidator',
    },
]

LANGUAGE_CODE = 'bg'

LANGUAGES = (
    ('en-us', _('English')),
    ('bg', _('Bulgarian')),
)

TIME_ZONE = 'Europe/Sofia'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users_app.UserApp'

LOGIN_URL = reverse_lazy('sign-in-user')
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')

PASSWORD_RESET_TIMEOUT = 3 * 60 * 60

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

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': de_config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': de_config('CLOUDINARY_API_KEY'),
    'API_SECRET': de_config('CLOUDINARY_API_SECRET'),
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE.get('CLOUD_NAME'),
    api_key=CLOUDINARY_STORAGE.get('API_KEY'),
    api_secret=CLOUDINARY_STORAGE.get('API_SECRET'),
)

EMAIL_BACKEND = de_config('EMAIL_BACKEND')
EMAIL_HOST = de_config('EMAIL_HOST')
EMAIL_HOST_USER = de_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = de_config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = de_config('EMAIL_PORT')
EMAIL_USE_TLS = de_config('EMAIL_USE_TLS')
# SERVER_EMAIL = de_config('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = f'Леки походи в планината <{EMAIL_HOST_USER}>'

CELERY_BROKER_URL = de_config('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = de_config('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# CELERY_TIMEZONE = 'Europe/Sofia'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": de_config('CELERY_BROKER_URL', 'redis://localhost:6379'),
    }
}

ADMINS = []
for admin in de_config('ADMINS', 'Admin,admin@admin.bg').split(' | '):
    ADMINS.append(tuple(admin.split(',')))

if not os.path.exists('Logs'):
    os.mkdir('Logs')

FILES_LOGGING_PATH = BASE_DIR / 'Logs'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} -> [{levelname}] ({name}.{module}.{funcName}): {message}',
            'style': '{',
            'datefmt': "%Y/%m/%d %H:%M:%S"
        },
        'simple': {
            'format': '[{levelname}]: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
        'file_warning_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': FILES_LOGGING_PATH / f'warning-{datetime.date.today().strftime("%m-%d-%Y")}.log',
            'level': 'WARNING',
            'mode': 'a',
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 5,  # 5 MiB
        },
        'file_info_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': FILES_LOGGING_PATH / f'info-{datetime.date.today().strftime("%m-%d-%Y")}.log',
            'level': 'INFO',
            'mode': 'a',
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 5,  # 5 MiB
        },
        'celery_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': FILES_LOGGING_PATH / f'celery-{datetime.date.today().strftime("%m-%d-%Y")}.log',
            'level': 'INFO',
            'mode': 'a',
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 5,  # 5 MiB
        },
        'mail_admin': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_info_handler', 'console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admin', 'file_info_handler', 'file_warning_handler', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['mail_admin', 'file_info_handler', 'file_warning_handler', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO' if DEBUG else 'WARNING',
        },
        'django.server': {
            'handlers': ['mail_admin', 'file_info_handler', 'file_warning_handler'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['celery_handler', ],
            'level': 'INFO'
        },
        'celery.task': {
            'handlers': ['celery_handler', ],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
