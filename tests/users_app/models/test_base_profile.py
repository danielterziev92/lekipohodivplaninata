from django.core.exceptions import ValidationError
from django.test import TestCase

from lekipohodivplaninata.users_app.models import UserApp, BaseProfile


class TestBaseProfile(TestCase):
    VALID_USER_APP_DATA = {
        'email': 'test@example.com',
        'password': 'password',
    }

    VALID_BASE_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '+359888998899'
    }

    def _create_and_save_base_profile(self, data):
        user_id = UserApp.objects.create(**self.VALID_USER_APP_DATA)
        user = BaseProfile(**data, user_id=user_id)
        user.full_clean()
        user.save()
        return user

    def test_create__when_valid_data__expect_to_be_created(self):
        user = self._create_and_save_base_profile(self.VALID_BASE_PROFILE_DATA)

    def test_create__when_first_name_with_one_more_character__expect_to_raise_exception(self):
        first_name = 'T' * BaseProfile.FIRST_NAME_MAX_LENGTH + 'T'
        with self.assertRaises(ValidationError):
            user_data = {**self.VALID_BASE_PROFILE_DATA, 'first_name': first_name}
            user = self._create_and_save_base_profile(user_data)

    def test_create__when_last_name_with_one_more_character__expect_to_raise_exception(self):
        last_name = 'T' * BaseProfile.LAST_NAME_MAX_LENGTH + 'T'
        with self.assertRaises(ValidationError):
            user_data = {**self.VALID_BASE_PROFILE_DATA, 'last_name': last_name}
            user = self._create_and_save_base_profile(user_data)

    def test_create__when_phone_number_with_one_more_character__expect_to_raise_exception(self):
        phone_number = '1' * BaseProfile.PHONE_NUMBER_MAX_LENGTH + '1'
        with self.assertRaises(ValidationError):
            user_data = {**self.VALID_BASE_PROFILE_DATA, 'phone_number': phone_number}
            user = self._create_and_save_base_profile(user_data)

    def test_first_name_prop__when_create_user_with_valid_data__expect_to_return_first_name(self):
        user = self._create_and_save_base_profile(self.VALID_BASE_PROFILE_DATA)

        self.assertEqual(self.VALID_BASE_PROFILE_DATA['first_name'], user.get_first_name)

    def test_last_name_prop__when_create_user_with_valid_data__expect_to_return_last_name(self):
        user = self._create_and_save_base_profile(self.VALID_BASE_PROFILE_DATA)

        self.assertEqual(self.VALID_BASE_PROFILE_DATA['last_name'], user.get_last_name)

    def test_full_name_prop__when_create_user_with_valid_data__expect_to_return_full_name(self):
        user = self._create_and_save_base_profile(self.VALID_BASE_PROFILE_DATA)

        full_name = f'{self.VALID_BASE_PROFILE_DATA["first_name"]} {self.VALID_BASE_PROFILE_DATA["last_name"]}'
        self.assertEqual(full_name, user.get_full_name)

    def test_email_prop__when_create_user_with_valid_data__expect_to_return_email(self):
        user = self._create_and_save_base_profile(self.VALID_BASE_PROFILE_DATA)

        self.assertEqual(self.VALID_USER_APP_DATA['email'], user.get_email)
