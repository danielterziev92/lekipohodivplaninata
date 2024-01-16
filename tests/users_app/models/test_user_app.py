from django.core.exceptions import ValidationError
from django.test import TestCase

from lekipohodivplaninata.users_app.models import UserApp
from tests.valid_data_for_test import ValidDataForTest


class UserAppModelForTest(TestCase, ValidDataForTest):
    VALID_USER_APP_DATA = {
        'email': 'test@example.com',
        'password': 'password',
    }

    def _create_user(self, data, **kwargs):
        return UserApp(**data, **kwargs)

    def test_create__when_valid_data__expect_to_be_created(self):
        user = self._create_user(self.USER_MODEL_DATA)
        user.full_clean()
        user.save()

        self.assertIsNotNone(user.pk)

    def test_crate__when_already_exists__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            user1 = self._create_user(self.USER_MODEL_DATA)
            user1.full_clean()
            user1.save()
            user2 = self._create_user(self.USER_MODEL_DATA)
            user2.full_clean()
            user2.save()

    def test_create__when_email_is_none__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            user = self._create_user(
                {
                    'password': self.USER_MODEL_DATA['password'],
                    'email': None
                }
            )
            user.full_clean()
            user.save()

    def test_create__when_password_is_none__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            user = self._create_user(
                {
                    'email': self.USER_MODEL_DATA['email'],
                    'password': None
                }
            )
            user.full_clean()
            user.save()
