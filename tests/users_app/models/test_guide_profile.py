from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from lekipohodivplaninata.users_app.models import UserApp, BaseProfile, GuideProfile
from tests.valid_data_for_test import ValidDataForTest


class GuideProfileModelForTest(TestCase, ValidDataForTest):
    def _create_and_save_user_data(self, data):
        user_app = UserApp.objects.create(**self.USER_MODEL_DATA)
        base_profile = BaseProfile.objects.create(user_id=user_app, **self.BASE_MODEL_DATA)
        guide_profile = GuideProfile.objects.create(user_id=user_app, profile_id=base_profile, **data)
        guide_profile.full_clean()
        guide_profile.save()
        return guide_profile

    def test_create__when_valid_data__expect_to_be_created(self):
        self._create_and_save_user_data(self.GUIDE_MODEL_DATA)
        self.assertEqual(UserApp.objects.count(), 1)

    def test_creat__when_do_not_have_avatar__expect_to_raise_exception(self):
        avatar = None
        with self.assertRaises(ValidationError):
            user_data = {**self.GUIDE_MODEL_DATA, 'avatar': avatar}
            self._create_and_save_user_data(user_data)

    def test_create__when_do_not_have_date_of_birth__expect_to_raise_exception(self):
        date_of_birth = None
        with self.assertRaises(IntegrityError):
            user_data = {**self.GUIDE_MODEL_DATA, 'date_of_birth': date_of_birth}
            self._create_and_save_user_data(user_data)

    def test_create__when_do_not_have_description__expect_to_raise_exception(self):
        description = None
        with self.assertRaises(IntegrityError):
            user_data = {**self.GUIDE_MODEL_DATA, 'description': description}
            self._create_and_save_user_data(user_data)

    def test_create__when_do_not_have_certificate__expect_to_raise_exception(self):
        certificate = None
        with self.assertRaises(ValidationError):
            user_data = {**self.GUIDE_MODEL_DATA, 'certificate': certificate}
            self._create_and_save_user_data(user_data)
