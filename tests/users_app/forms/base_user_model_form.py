from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.base.models import BaseUserModel
from lekipohodivplaninata.users_app.forms import BaseUserModelForm, UserModelForm
from tests.valid_data_for_test import ValidDataForTest

UserModel = get_user_model()


class BaseUserModelFormForTest(TestCase, ValidDataForTest):
    def setUp(self):
        self.user = UserModel.objects.create_user(**self.USER_MODEL_DATA)

    def test_form__when_valid_data__expect_to_submit(self):
        form = BaseUserModelForm(data={**self.BASE_MODEL_DATA, 'user_id': self.user})
        is_valid = form.is_valid()
        message = form.errors

        self.assertTrue(is_valid)
        self.assertEqual(len(message), 0)

    def test_form__when_user_id_is_none__expect_to_return_message(self):
        form = BaseUserModelForm(data=self.BASE_MODEL_DATA)
        is_valid = form.is_valid()
        message = form.errors['user_id'][0]

        expected_error_message = form.fields['user_id'].error_messages['required']

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, message)

    def test_form__when_first_name_is_none__expect_to_return_message(self):
        form = BaseUserModelForm(data={**self.BASE_MODEL_DATA, 'user_id': self.user, 'first_name': None})
        is_valid = form.is_valid()
        message = form.errors['first_name'][0]

        expected_error_message = form.fields['first_name'].error_messages['required']

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, message)

    def test_form__when_first_name_one_more_character__expect_to_return_message(self):
        first_name = 'T' * (BaseUserModel.FIRST_NAME_MAX_LENGTH + 1)
        form = BaseUserModelForm(data={**self.BASE_MODEL_DATA, 'user_id': self.user, 'first_name': first_name})
        is_valid = form.is_valid()
        message = form.errors['first_name'][0]

        expected_error_message = \
            (f'Уверете се, че тази стойност има най-много {BaseUserModel.FIRST_NAME_MAX_LENGTH} знака (тя има '
             f'{BaseUserModel.FIRST_NAME_MAX_LENGTH + 1}).')

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, message)

    def test_form_when_last_name_is_none__expect_to_return_message(self):
        form = BaseUserModelForm(data={**self.BASE_MODEL_DATA, 'user_id': self.user, 'last_name': None})
        is_valid = form.is_valid()
        message = form.errors['last_name'][0]

        expected_error_message = form.fields['last_name'].error_messages['required']

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, message)

    def test_form_when_last_name_one_more_character__expect_to_return_message(self):
        last_name = 'T' * (BaseUserModel.LAST_NAME_MAX_LENGTH + 1)
        form = BaseUserModelForm(data={**self.BASE_MODEL_DATA, 'user_id': self.user, 'last_name': last_name})
        is_valid = form.is_valid()
        message = form.errors['last_name'][0]

        expected_error_message = \
            (f'Уверете се, че тази стойност има най-много {BaseUserModel.LAST_NAME_MAX_LENGTH} знака (тя има '
             f'{BaseUserModel.LAST_NAME_MAX_LENGTH + 1}).')

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, message)

    def test_form_when_phone_number_is_none__expect_to_return_message(self):
        form = BaseUserModelForm(data={**self.BASE_MODEL_DATA, 'user_id': self.user, 'phone_number': None})
        is_valid = form.is_valid()
        message = form.errors['phone_number'][0]

        expected_error_message = form.fields['phone_number'].error_messages['required']

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, message)

    def test_form__when_phone_number_one_more_character_and_start_with_plus__expect_to_return_message(self):
        phone_number = '+' + '1' * BaseUserModelForm.PHONE_NUMBER_MAX_LENGTH
        form = BaseUserModelForm(data={**self.BASE_MODEL_DATA, 'user_id': self.user, 'phone_number': phone_number})
        is_valid = form.is_valid()
        message = form.errors['phone_number'][0]

        expected_error_message = \
            (f'Уверете се, че тази стойност има най-много {BaseUserModelForm.PHONE_NUMBER_MAX_LENGTH} знака (тя има '
             f'{BaseUserModelForm.PHONE_NUMBER_MAX_LENGTH + 1}).')

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, message)
