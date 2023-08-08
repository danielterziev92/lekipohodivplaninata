import os
import pathlib
import smtplib

import cloudinary.api
import django
import redis
from cloudinary.exceptions import Error
from decouple import config
from django.core.management.base import BaseCommand


class CheckConnectionsCommand(BaseCommand):
    help = 'Checks connections'

    def handle(self, *args, **options):
        methods = [getattr(self, method) for method in dir(self) if
                   callable(getattr(self, method)) and method.startswith("check_")]

        try:
            for method in methods:
                method()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connections check failed: {e}"))
            raise SystemExit(1)

    @staticmethod
    def _load_env_variables():
        env_folder_path = pathlib.Path(__file__).resolve().parent.parent.parent
        dot_env_path = env_folder_path / '.env'

        if not dot_env_path.exists():
            raise Exception('The path does not exist')

        return config('SITE_DOMAIN') is not None

    def check_env_variables(self):
        env_loaded = self._load_env_variables()

        if env_loaded:
            self.stdout.write(self.style.SUCCESS("Environment variables loaded successfully."))
        else:
            self.stdout.write(self.style.ERROR("Environment variables not loaded."))

    def check_database_connection(self):
        from django.db import connection

        try:
            django.setup()
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('Database connection is successful.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database connection failed: {e}'))
            raise

    def check_redis_connection(self):
        try:
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
            redis_client = redis.from_url(redis_url)
            redis_client.ping()
            self.stdout.write(self.style.SUCCESS('Redis connection is successful.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Redis connection failed: {e}'))
            raise

    def check_cloudinary_connection(self):
        try:
            cloudinary.config(
                cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
                api_key=os.environ.get('CLOUDINARY_API_KEY'),
                api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
            )
            cloudinary.api.ping()
            self.stdout.write(self.style.SUCCESS('Cloudinary connection is successful.'))
        except Error as e:
            self.stdout.write(self.style.ERROR(f'Cloudinary connection failed: {e}'))
            raise

    def check_test_smtp_connection(self):
        try:
            server = smtplib.SMTP(os.environ.get('EMAIL_HOST'), int(os.environ.get('EMAIL_PORT')))
            server.starttls()
            server.login(os.environ.get('EMAIL_HOST_USER'), os.environ.get('EMAIL_HOST_PASSWORD'))
            server.quit()
            self.stdout.write(self.style.SUCCESS("SMTP server connection successful."))
        except smtplib.SMTPServerDisconnected:
            self.stderr.write("SMTP server disconnected.")
        except smtplib.SMTPConnectError as e:
            self.stderr.write(f"SMTP connection error: {e}")
        except Exception as e:
            self.stderr.write(f"An error occurred: {e}")
