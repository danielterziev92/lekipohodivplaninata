import os
import smtplib

import cloudinary.api
import django
from cloudinary.exceptions import Error
from django.core.management.base import BaseCommand


class CheckConnectionsCommand(BaseCommand):
    help = 'Checks connections'

    def handle(self, *args, **options):
        # Get all methods in the class
        methods = [getattr(self, method) for method in dir(self) if
                   callable(getattr(self, method)) and method.startswith("check_")]

        try:
            for method in methods:
                method()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connections check failed: {e}"))
            raise SystemExit(1)

    def check_database_connection(self):
        from django.db import connection

        try:
            django.setup()
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('Database connection is successful.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database connection failed: {e}'))
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
