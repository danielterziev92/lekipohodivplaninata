import datetime
import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path

import cloudinary
from django.urls import reverse_lazy

import lekipohodivplaninata.users_app.validators

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = bool(os.environ.get('DEBUG'))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

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
                'lekipohodivplaninata.core.context_processors.get_contacts',
            ],
        },
    },
]

WSGI_APPLICATION = 'lekipohodivplaninata.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
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

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "templates/static/",
]

# STATIC_ROOT = 'templates/static/'

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'templates/media')

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users_app.UserApp'

LOGIN_URL = reverse_lazy('sign-in-user')
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')

PASSWORD_RESET_TIMEOUT = 3 * 60 * 60

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = f'Леки походи в планината <{EMAIL_HOST_USER}>'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Europe/Sofia'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get('CELERY_BROKER_URL'),
    }
}

ADMINS = []
for admin in os.environ.get('ADMINS').split(' | '):
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
        'mail_admin': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'WARNING',
            'include_html': True,
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_info_handler', 'console' if DEBUG else ''],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admin', 'file_info_handler', 'file_warning_handler', 'console' if DEBUG else ''],
            'level': 'INFO',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['mail_admin', 'file_info_handler', 'file_warning_handler', 'console' if DEBUG else ''],
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
        }
    }
}
