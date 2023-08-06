import datetime
import os
from pathlib import Path

from lekipohodivplaninata.settings import DEBUG

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ADMINS = []
for admin in os.environ.get('ADMINS', 'Admin,admin@admin.bg').split(' | '):
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
            'filename': FILES_LOGGING_PATH / f'celery-info-{datetime.date.today().strftime("%m-%d-%Y")}.log',
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
            'handlers': ['celery_handler'],
            'level': 'INFO'
        },
        'celery.task': {
            'handlers': ['celery_handler'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
