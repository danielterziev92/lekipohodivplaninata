from django.test import TestCase


class TestSettingsModel(TestCase):
    VALID_SOCIAL_MEDIA_DATA = {
        'name': 'Test',
        'url': 'https://example.com',
        'fontawesome_icon': 'fa-test',
        'icon_color': 'ffffff'
    }

    VALID_SETTINGS_DATA = {
        'phone_number': '+1234567890',
        'email_for_contact': 'test@example.com',
        'social_media': []
    }

    def _create_and_save_social_media(self, data):
        pass

    def _create_and_save_settings(self, data):
        pass

    def test_create__when_valid_data__expect_to_be_created(self):
        pass

    def test_create__when_phone_number_with_one_more_character__expect_to_raise_exception(self):
        pass

    def test_create__when_phone_number_is_null__expect_to_raise_exception(self):
        pass

    def test_create__when_email_for_contact_is_not_email__expect_to_raise_exception(self):
        pass

    def test_create__when_email_for_contact_is_null__expect_to_raise_exception(self):
        pass

    def test_create__when_social_media_is_null__expect_to_be_created(self):
        pass

    def test_create__when_delete_social_media__expect_to_still_have_data(self):
        pass

    def test_create__when_pass_different_object__expect_to_raise_exception(self):
        pass
