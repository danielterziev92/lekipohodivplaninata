from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

UserModel = get_user_model()


class SingInViewTest(TestCase):
    VALID_USER_APP_DATA = {
        'email': 'test@example.com',
        'password': 'Password123!.',
    }

    @staticmethod
    def _create_user_app(data):
        user_app = UserModel.objects.create_user(**data)
        return user_app

    def test_create_user_app__when_valid_data__expect_to_be_created(self):
        self._create_user_app(self.VALID_USER_APP_DATA)

        login_success = self.client.login(**self.VALID_USER_APP_DATA)
        self.assertTrue(login_success)

    def test_create_user_app__when_email_does_not_exist__expect_to_raise_exception(self):
        self._create_user_app(self.VALID_USER_APP_DATA)

        user_data = {**self.VALID_USER_APP_DATA, 'email': None}
        self.assertFalse(self.client.login(**user_data))

    def test_create_user_app__when_email_is_wrong__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_password_does_not_exist__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_password_is_wrong__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_email_and_password_is_none__expect_to_raise_exception(self):
        pass
