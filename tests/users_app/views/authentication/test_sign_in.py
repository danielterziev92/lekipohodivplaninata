from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class SingInViewTest(TestCase):
    VALID_USER_APP_DATA = {
        'email': 'test@example.com',
        'password': 'password',
    }

    def _create_user_app(self, data):
        user_app = UserModel.objects.create_user(**data)
        user_app.save()
        return user_app

    def test_create_user_app__when_valid_data__expect_to_be_created(self):
        pass

    def test_create_user_app__when_email_does_not_exist__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_email_is_wrong__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_password_does_not_exist__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_password_is_wrong__expect_to_raise_exception(self):
        pass

    def test_create_user_app__when_email_and_password_is_none__expect_to_raise_exception(self):
        pass
