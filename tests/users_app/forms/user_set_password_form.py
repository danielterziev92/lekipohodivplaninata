from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.users_app.forms import UserSetPasswordForm
from lekipohodivplaninata.users_app.models import BaseProfile
from tests.valid_data_for_test import ValidDataForTest

UserModel = get_user_model()


class UserSetPasswordFormForTest(TestCase, ValidDataForTest):
    VALID_DATA = {
        'new_password1': 'Password123.',
        'new_password2': 'Password123.',
    }

    def setUp(self):
        user = UserModel.objects.create_user(**self.USER_MODEL_DATA)
        user.save()

        base_profile = BaseProfile.objects.create(**self.BASE_MODEL_DATA, user_id=user)
        base_profile.save()

        self.user = base_profile

    def test_set_password__when_valid_data__expect_to_be_submitted(self):
        form = UserSetPasswordForm(data=self.VALID_DATA, user=self.user)
        is_valid = form.is_valid()

        self.assertTrue(is_valid)

    def test_set_password__when_password_mismatch__expert_to_return_message(self):
        form = UserSetPasswordForm(data={**self.VALID_DATA, 'new_password2': 'InvalidPassword'}, user=self.user)
        is_valid = form.is_valid()
        message = form.errors['new_password2'][0]
        expected_message = UserSetPasswordForm.MESSAGE['password_mismatch']

        self.assertFalse(is_valid)
        self.assertEqual(expected_message, message)
