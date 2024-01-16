from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from lekipohodivplaninata.users_app.models import BaseProfile
from tests.valid_data_for_test import ValidDataForTest

UserModel = get_user_model()


class BaseProfileModelForTest(TestCase, ValidDataForTest):
    def _create_and_save_base_profile(self, data):
        user_id = UserModel.objects.create(**self.USER_MODEL_DATA)
        user = BaseProfile(**data, user_id=user_id)
        user.full_clean()
        user.save()
        return user

    def test_create__when_valid_data__expect_to_be_created(self):
        self._create_and_save_base_profile(self.BASE_MODEL_DATA)
        self.assertEqual(BaseProfile.objects.count(), 1)

    def test_create__when_first_name_with_one_more_character__expect_to_raise_exception(self):
        first_name = 'T' * BaseProfile.FIRST_NAME_MAX_LENGTH + 'T'
        with self.assertRaises(ValidationError):
            user_data = {**self.BASE_MODEL_DATA, 'first_name': first_name}
            self._create_and_save_base_profile(user_data)

    def test_create__when_last_name_with_one_more_character__expect_to_raise_exception(self):
        last_name = 'T' * BaseProfile.LAST_NAME_MAX_LENGTH + 'T'
        with self.assertRaises(ValidationError):
            user_data = {**self.BASE_MODEL_DATA, 'last_name': last_name}
            self._create_and_save_base_profile(user_data)

    def test_create__when_phone_number_with_one_more_character__expect_to_raise_exception(self):
        phone_number = '1' * BaseProfile.PHONE_NUMBER_MAX_LENGTH + '1'
        with self.assertRaises(ValidationError):
            user_data = {**self.BASE_MODEL_DATA, 'phone_number': phone_number}
            self._create_and_save_base_profile(user_data)

    def test_first_name_prop__when_create_user_with_valid_data__expect_to_return_first_name(self):
        user = self._create_and_save_base_profile(self.BASE_MODEL_DATA)

        self.assertEqual(self.BASE_MODEL_DATA['first_name'], user.get_first_name)

    def test_last_name_prop__when_create_user_with_valid_data__expect_to_return_last_name(self):
        user = self._create_and_save_base_profile(self.BASE_MODEL_DATA)

        self.assertEqual(self.BASE_MODEL_DATA['last_name'], user.get_last_name)

    def test_full_name_prop__when_create_user_with_valid_data__expect_to_return_full_name(self):
        user = self._create_and_save_base_profile(self.BASE_MODEL_DATA)

        full_name = f'{self.BASE_MODEL_DATA["first_name"]} {self.BASE_MODEL_DATA["last_name"]}'
        self.assertEqual(full_name, user.get_full_name)

    def test_email_prop__when_create_user_with_valid_data__expect_to_return_email(self):
        user = self._create_and_save_base_profile(self.BASE_MODEL_DATA)

        self.assertEqual(self.USER_MODEL_DATA['email'], user.get_email)

    def test__when_create_base_profile_and_delete_user_id__expect_to_delete_both(self):
        base_profile = self._create_and_save_base_profile(self.BASE_MODEL_DATA)
        user_app = base_profile.user_id

        self.assertTrue(UserModel.objects.filter(pk=user_app.pk).exists())
        self.assertTrue(BaseProfile.objects.filter(pk=base_profile.pk).exists())

        user_app.delete()

        self.assertFalse(UserModel.objects.filter(pk=user_app.pk).exists())
        self.assertFalse(BaseProfile.objects.filter(pk=base_profile).exists())
