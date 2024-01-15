from django.contrib.auth import get_user_model
from django.test import TestCase

UserModel = get_user_model()


class SignInFormTest(TestCase):
    VALID_DATA = {
        'email': 'test@example.com',
        'password': 'Password123.',
    }

    def setUp(self):
        self.user = UserModel.objects.create_user(**self.VALID_DATA)

    def test_form__when_valid_data__expect_to_be_submitted(self):
        pass

    def test_form__when_email_is_not_email__expect_to_return_message(self):
        pass

    def test_form__when_email_is_none__expect_to_return_message(self):
        pass

    def test_form__when_password_is_not_correct__expect_to_return_message(self):
        pass

    def test_form__when_password_is_none__expect_to_return_message(self):
        pass
