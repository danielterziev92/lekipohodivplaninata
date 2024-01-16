from django.test import TestCase

from lekipohodivplaninata.users_app.forms import SignUpFormUser


class SignUpFormTest(TestCase):
    VALIDA_DATA = {
        'email': 'test@example.com',
        'password1': 'Password123.',
        'password2': 'Password123.',
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '1234567890',
    }

    def test_sign_up__when_valid_data__expect_to_create_user(self):
        pass

    def test_sign_up__when_email_already_exist__expect_to_return_message(self):
        pass

    def test_sign_up__when_password_does_not_match__expect_to_return_message(self):
        pass
