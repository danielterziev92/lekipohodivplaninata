from django.contrib.auth import get_user_model
from django.test import TestCase

from lekipohodivplaninata.base.models import BaseUserModel
from lekipohodivplaninata.users_app.forms import SignUpFormUser

UserModel = get_user_model()


class SignUpFormTest(TestCase):
    VALIDA_DATA = {
        'email': 'test@example.com',
        'password1': 'Password123.',
        'password2': 'Password123.',
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '1234567890',
    }

    def test_sign_up__when_valid_data__expect_to_create_user(self):
        form = SignUpFormUser(data=self.VALIDA_DATA)
        is_valid = form.is_valid()

        self.assertTrue(is_valid)

    def test_sign_up__when_email_already_exist__expect_to_return_message(self):
        user = UserModel.objects.create_user(email=self.VALIDA_DATA['email'], password=self.VALIDA_DATA['password1'])
        user.save()
        base_user = BaseUserModel.objects.create(user_id=user,
                                                 first_name=self.VALIDA_DATA['first_name'],
                                                 last_name=self.VALIDA_DATA['last_name'],
                                                 phone_number=self.VALIDA_DATA['phone_number'])
        base_user.save()

        form2 = SignUpFormUser(data=self.VALIDA_DATA)
        is_form2_valid = form2.is_valid()

        self.assertFalse(is_form2_valid)

    def test_sign_up__when_password_does_not_match__expect_to_return_message(self):
        pass
