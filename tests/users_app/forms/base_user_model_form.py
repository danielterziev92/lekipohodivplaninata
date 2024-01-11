from django.test import TestCase


class BaseUserModelFormTest(TestCase):
    VALID_FORM_DATA = {
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '+1234567890',
    }

    def test_form_rendering(self):
        pass

    def test_form__when_valid_data__expect_to_submit(self):
        pass

    def test_form__when_first_name_one_more_character__expect_to_return_message(self):
        pass

    def test_form_when_last_name_one_more_character__expect_to_return_message(self):
        pass

    def test_form__when_phone_number_one_more_character__expect_to_return_message(self):
        pass
