from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.users_app.forms import BaseUserModelForm

UserModel = get_user_model()


class BaseUserModelFormTest(TestCase):
    VALID_USER_DATA = {
        'email': 'test@example.com',
        'password': 'Password123.'
    }

    VALID_FORM_DATA = {
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '+123456789000',
    }

    def setUp(self):
        self.user = UserModel.objects.create_user(**self.VALID_USER_DATA)

    def test_form__when_valid_data__expect_to_submit(self):
        form = BaseUserModelForm(data={**self.VALID_FORM_DATA, 'user_id': self.user})
        is_valid = form.is_valid()
        message = form.errors

        self.assertTrue(is_valid)
        self.assertEqual(len(message), 0)

    def test_form__when_first_name_one_more_character__expect_to_return_message(self):
        pass

    def test_form_when_last_name_one_more_character__expect_to_return_message(self):
        pass

    def test_form__when_phone_number_one_more_character__expect_to_return_message(self):
        pass
