from django.core.exceptions import ValidationError
from django.test import TestCase

from lekipohodivplaninata.users_app.models import UserApp


class TestUserApp(TestCase):
    VALID_USER_APP_DATA = {
        'email': 'test@example.com',
        'password': 'password',
    }

    def _create_user(self, data, **kwargs):
        return UserApp(**data, **kwargs)

    def test_create__when_valid_data__expect_to_be_created(self):
        user = self._create_user(self.VALID_USER_APP_DATA)
        user.full_clean()
        user.save()

        self.assertIsNotNone(user.pk)

    def test_crate__when_already_exists__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            user1 = self._create_user(self.VALID_USER_APP_DATA)
            user1.full_clean()
            user1.save()
            user2 = self._create_user(self.VALID_USER_APP_DATA)
            user2.full_clean()
            user2.save()

    def test_create__when_email_is_none__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            user = self._create_user(
                {
                    'password': self.VALID_USER_APP_DATA['password'],
                    'email': None
                }
            )
            user.full_clean()
            user.save()

    def test_create__when_password_is_none__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            user = self._create_user(
                {
                    'email': self.VALID_USER_APP_DATA['email'],
                    'password': None
                }
            )
            user.full_clean()
            user.save()
