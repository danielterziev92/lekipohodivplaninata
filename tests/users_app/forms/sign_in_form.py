from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.users_app.forms import SignInForm

UserModel = get_user_model()


class SignInFormTest(TestCase):
    VALID_DATA = {
        'username': 'test@example.com',
        'password': 'Password123.',
    }

    def setUp(self):
        user_data = {**self.VALID_DATA, 'email': self.VALID_DATA['username']}
        del user_data['username']
        self.user = UserModel.objects.create_user(**user_data)

    def test_form__when_valid_data__expect_to_be_submitted(self):
        form = SignInForm(data=self.VALID_DATA)
        is_valid = form.is_valid()

        self.assertTrue(is_valid)

    def test_form__when_email_is_not_email__expect_to_return_message(self):
        form = SignInForm(data={**self.VALID_DATA, 'username': 'invalid_email'})
        is_valid = form.is_valid()
        message = form.errors['username'][0]
        expected_message = form.fields['username'].validators[0].message

        self.assertFalse(is_valid)
        self.assertEqual(expected_message, message)

    def test_form__when_email_is_none__expect_to_return_message(self):
        form = SignInForm(data={**self.VALID_DATA, 'username': None})
        is_valid = form.is_valid()
        message = form.errors['username'][0]
        expected_message = form.fields['username'].error_messages['required']

        self.assertFalse(is_valid)
        self.assertEqual(expected_message, message)

    def test_form__when_email_does_not_exist__expect_to_return_message(self):
        form = SignInForm(data={'username': 'test2@example.com', 'password': 'Password1.'})
        is_valid = form.is_valid()
        message = form.errors['username'][0]
        expected_message = SignInForm.MESSAGES['user_does_not_exist']

        self.assertFalse(is_valid)
        self.assertEqual(expected_message, message)

    def test_form__when_password_is_not_correct__expect_to_return_message(self):
        form = SignInForm(data={**self.VALID_DATA, 'password': 'password'})
        is_valid = form.is_valid()
        message = form.errors['password'][0]
        expected_message = SignInForm.MESSAGES['invalid_password']

        self.assertFalse(is_valid)
        self.assertEqual(expected_message, message)

    def test_form__when_password_is_none__expect_to_return_message(self):
        form = SignInForm(data={**self.VALID_DATA, 'password': None})
        is_valid = form.is_valid()
        message = form.errors['password'][0]
        expected_message = form.fields['password'].error_messages['required']

        self.assertFalse(is_valid)
        self.assertEqual(expected_message, message)
