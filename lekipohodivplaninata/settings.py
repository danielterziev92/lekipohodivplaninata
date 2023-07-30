import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if os.environ.get('DJANGO_ENV') == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *

DEFAULT_PROTOCOL = 'http'

LOGO = 'https://res.cloudinary.com/doh9wk7mw/image/upload/v1685648111/Logo_bfqo11.png'
