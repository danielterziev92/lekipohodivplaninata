from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from tests.valid_data_for_test import ValidDataForTest

UserModel = get_user_model()


class SingInViewForTest(TestCase, ValidDataForTest):
    VALID_USER_APP_DATA = {
        'email': 'test@example.com',
        'password': 'Password123!.',
    }

    @staticmethod
    def _create_user_app(data):
        user_app = UserModel.objects.create_user(**data)
        return user_app

    def test_create_user_app__when_valid_data__expect_to_be_created(self):
        self._create_user_app(self.USER_MODEL_DATA)

        login_success = self.client.login(**self.USER_MODEL_DATA)
        self.assertTrue(login_success)

    def test_create_user_app__when_email_does_not_exist__expect_to_raise_exception(self):
        self._create_user_app(self.USER_MODEL_DATA)

        user_data = {**self.USER_MODEL_DATA, 'email': None}
        self.assertFalse(self.client.login(**user_data))

    def test_create_user_app__when_email_is_wrong__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_password_does_not_exist__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_password_is_wrong__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_email_and_password_is_none__expect_to_raise_exception(self):
        pass
