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

    def _create_base_profile(self, data, **kwargs):
        user_id = UserApp.objects.create(**self.VALID_USER_APP_DATA)
        base_profile_data = {
            **data,
            **kwargs
        }
        return BaseProfile(
            **base_profile_data,
            user_id=user_id
        )

    def test_create__when_valid_data__expect_to_be_created(self):
        user = self._create_base_profile(self.VALID_BASE_PROFILE_DATA)
        user.full_clean()
        user.save()

    def test_create__when_first_name_with_one_more_character__expect_to_raise_exception(self):
        first_name = 'T' * BaseProfile.FIRST_NAME_MAX_LENGTH + 'T'
        with self.assertRaises(ValidationError):
            user = self._create_base_profile(
                self.VALID_BASE_PROFILE_DATA,
                first_name=first_name,
            )
            user.full_clean()
            user.save()

    def test_create__when_last_name_with_one_more_character__expect_to_raise_exception(self):
        last_name = 'T' * BaseProfile.LAST_NAME_MAX_LENGTH + 'T'
        with self.assertRaises(ValidationError):
            user = self._create_base_profile(
                self.VALID_BASE_PROFILE_DATA,
                last_name=last_name,
            )
            user.full_clean()
            user.save()

    def test_create__when_phone_number_with_one_more_character__expect_to_raise_exception(self):
        phone_number = '1' * BaseProfile.PHONE_NUMBER_MAX_LENGTH + '1'
        with self.assertRaises(ValidationError):
            user = self._create_base_profile(
                self.VALID_BASE_PROFILE_DATA,
                phone_number=phone_number,
            )
            user.full_clean()
            user.save()
