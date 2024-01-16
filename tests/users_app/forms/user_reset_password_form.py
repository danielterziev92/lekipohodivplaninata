from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.base.models import BaseUserModel
from lekipohodivplaninata.users_app.forms import UserResetPasswordForm
from tests.valid_data_for_test import ValidDataForTest

UserModel = get_user_model()


class UserResetPasswordFormForTest(TestCase, ValidDataForTest):
    VALID_DATA = {'email': 'test@example.com'}

    def setUp(self):
        user = UserModel.objects.create_user(**self.USER_MODEL_DATA)
        user.save()

        self.user = BaseUserModel(**self.BASE_MODEL_DATA, user_id=user)
        self.user.save()

    def test_reset_password__when_valid_data__expert_to_be_submitted(self):
        form = UserResetPasswordForm(data=self.VALID_DATA)
        is_valid = form.is_valid()

        self.assertTrue(is_valid)

    def test_reset_password__when_email_does_not_exist(self):
        form = UserResetPasswordForm(data={'email': 'invalid_test@example.com'})
        is_valid = form.is_valid()
        message = form.errors['email'][0]
        expected_message = UserResetPasswordForm.MESSAGE['email_does_not_exist']

        self.assertFalse(is_valid)
        self.assertEqual(expected_message, message)
