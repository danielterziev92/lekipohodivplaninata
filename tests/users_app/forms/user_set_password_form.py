from django.test import TestCase


class UserSetPasswordFormTest(TestCase):
    VALID_DATA = {
        'password1': 'Password123.',
        'password2': 'Password123.',
    }

    def test_set_password__when_valid_data__expect_to_be_submitted(self):
        pass

    def test_set_password__when_password_mismatch__expert_to_return_message(self):
        pass
