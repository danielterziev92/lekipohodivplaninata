from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.base.models import BaseUserModel

UserModel = get_user_model()


class UserResetPasswordFormTest(TestCase):
    USED_MODEL_DATA = {
        'email': 'test@example.com',
        'password': 'Password123.'
    }

    BASE_MODEL_DATA = {
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '0123456789'
    }

    VALID_DATA = {'email': 'test@example.com'}

    def setUp(self):
        user = UserModel.objects.create_user(**self.USED_MODEL_DATA)
        user.save()

        self.user = BaseUserModel(**self.BASE_MODEL_DATA, user_id=user)
        self.user.save()

    def test_reset_password__when_valid_data__expert_to_be_submitted(self):
        pass

    def test_reset_password__when_email_does_not_exist(self):
        pass
