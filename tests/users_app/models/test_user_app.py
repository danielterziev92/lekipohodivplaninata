from django.db import IntegrityError
from django.test import TestCase

from lekipohodivplaninata.users_app.models import UserApp


class TestUserApp(TestCase):
    VALID_USER_APP_DATA = {
        'email': 'test@example.com',
        'password': 'password',
    }

    def setUp(self):
        self.test_user = UserApp.objects.create(
            email=self.VALID_USER_APP_DATA['email'],
            password=self.VALID_USER_APP_DATA['password'],
        )

    def test_create__when_valid_data__expect_to_be_created(self):
        user = self.test_user

        self.assertIsNotNone(user.pk)

    def test_crate__when_already_exists__expect_to_raise_exception(self):
        with self.assertRaises(IntegrityError):
            UserApp.objects.create(
                email=self.VALID_USER_APP_DATA['email'],
                password=self.VALID_USER_APP_DATA['password'],
            )

    def test_create__when_email_is_none__expect_to_raise_exception(self):
        with self.assertRaises(IntegrityError):
            UserApp.objects.create(
                email=None,
                password=self.VALID_USER_APP_DATA['password'],
            )

    def test_create__when_password_is_none__expect_to_raise_exception(self):
        with self.assertRaises(IntegrityError):
            UserApp.objects.create(
                email=self.VALID_USER_APP_DATA['email'],
                password=None,
            )
