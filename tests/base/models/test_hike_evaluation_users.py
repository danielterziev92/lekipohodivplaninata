from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.base.models import HikeEvaluationUsers
from lekipohodivplaninata.users_app.models import BaseProfile
from tests.valid_data_for_test import ValidDataForTest

UserModel = get_user_model()


class HikeEvaluationUsersModel(TestCase, ValidDataForTest):
    VALID_USER_DATA = {
        'email': 'test@test.com',
        'password': 'Test123@',
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '+1234567890',
    }

    VALID_HIKE_EVALUATION_USERS_DATA = {
        'assessment': 5,
        'comment': 'Test Comment',
        'user_id': None,
    }

    def _create_and_save_base_profile(self):
        user_app = UserModel.objects.create_user(**self.USER_MODEL_DATA)
        base_profile = BaseProfile(user_id=user_app, **self.BASE_MODEL_DATA)
        base_profile.save()
        return base_profile

    def _create_and_save_hike_evaluation_user(self, data):
        hike_evaluation_users = HikeEvaluationUsers.objects.create(**data)
        hike_evaluation_users.full_clean()
        hike_evaluation_users.save()
        return hike_evaluation_users

    def test_create_hike_evaluation_users__with_valid_data__expect_to_be_created(self):
        base_profile = self._create_and_save_base_profile()
        hike_evaluation_users_data = {**self.VALID_HIKE_EVALUATION_USERS_DATA, 'user_id': base_profile}

        hike_evaluation_users = self._create_and_save_hike_evaluation_user(hike_evaluation_users_data)
        self.assertEqual(HikeEvaluationUsers.objects.count(), 1)
        self.assertEqual(hike_evaluation_users.user_id, base_profile)

    def test_create_hike_evaluation_users__without_base_profile__expect_to_be_created(self):
        hike_evaluation_users_data = {**self.VALID_HIKE_EVALUATION_USERS_DATA}

        hike_evaluation_users = self._create_and_save_hike_evaluation_user(hike_evaluation_users_data)
        self.assertEqual(HikeEvaluationUsers.objects.count(), 1)
        self.assertEqual(hike_evaluation_users.user_id, self.VALID_HIKE_EVALUATION_USERS_DATA['user_id'])

    def test_create_hike_evaluation_users__with_valid_data_and_delete_base_profile__expect_to_be_deleted(self):
        base_profile = self._create_and_save_base_profile()
        hike_evaluation_users_data = {**self.VALID_HIKE_EVALUATION_USERS_DATA, 'user_id': base_profile}

        hike_evaluation_users = self._create_and_save_hike_evaluation_user(hike_evaluation_users_data)
        self.assertEqual(HikeEvaluationUsers.objects.count(), 1)
        self.assertEqual(hike_evaluation_users.user_id, base_profile)

        user_id = hike_evaluation_users.user_id
        self.assertTrue(UserModel.objects.filter(pk=user_id.pk).exists())
        self.assertTrue(BaseProfile.objects.filter(pk=base_profile.pk).exists())

        user_id.delete()

        self.assertFalse(UserModel.objects.filter(pk=user_id.pk).exists())
        self.assertFalse(BaseProfile.objects.filter(pk=base_profile.pk).exists())

        self.assertEqual(HikeEvaluationUsers.objects.filter(pk=hike_evaluation_users.pk).get().user_id, None)
