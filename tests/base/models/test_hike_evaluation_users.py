from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.base.models import HikeEvaluationUsers
from lekipohodivplaninata.users_app.models import BaseProfile

UserModel = get_user_model()


class HikeEvaluationUsersModel(TestCase):
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
    }

    def _create_and_save_hike_evaluation_user(self, data):
        email, password, *base_profile_data = self.VALID_USER_DATA.values()

        user_app = UserModel.objects.create_user(email=email, password=password)
        base_user = BaseProfile(user_id=user_app, **base_profile_data)

        hike_evaluation_user = HikeEvaluationUsers.objects.create(user_id=base_user, **data)
        hike_evaluation_user.full_clean()
        return hike_evaluation_user.save()

    def test_create__with_valid_data__expect_to_be_created(self):
        pass

    def test_create__without_base_profile__expect_to_be_created(self):
        pass

    def test_create__with_valid_data_and_delete_base_profile__expect_to_be_deleted(self):
        pass
