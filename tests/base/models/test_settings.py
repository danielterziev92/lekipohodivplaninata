from django.db import DataError
from django.test import TestCase
from django.db.models.fields.related_descriptors import ManyToManyDescriptor

from lekipohodivplaninata.base.models import SocialMedia, Settings


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

    @staticmethod
    def __create_and_save_social_media(data):
        social_media = SocialMedia.objects.create(**data)
        social_media.full_clean()
        social_media.save()
        return social_media

    def _create_and_save_settings(self, data):
        social_medias = [(self.__create_and_save_social_media(cur_data)) for cur_data in data['social_media']]
        del data['social_media']

        settings = Settings.objects.create(**data)
        settings.full_clean()
        settings.save()

        settings.social_media.set(social_medias)

        return settings

    def test_create__when_valid_data__expect_to_be_created(self):
        social_medias = [
            {**self.VALID_SOCIAL_MEDIA_DATA, 'name': 'Test1'},
            {**self.VALID_SOCIAL_MEDIA_DATA, 'name': 'Test2'},
            {**self.VALID_SOCIAL_MEDIA_DATA, 'name': 'Test3'},
        ]

        settings = self._create_and_save_settings({**self.VALID_SETTINGS_DATA, 'social_media': social_medias})

        self.assertEqual(Settings.objects.count(), 1)

        self.assertEqual(settings.phone_number, self.VALID_SETTINGS_DATA['phone_number'])

        self.assertTrue(settings.social_media.all().exists())

    def test_create__when_phone_number_with_one_more_character__expect_to_raise_exception(self):
        phone_number = '1' * (Settings.PHONE_NUMBER_MAX_LENGTH + 1)
        settings_data = {**self.VALID_SETTINGS_DATA, 'phone_number': phone_number}

        with self.assertRaises(DataError):
            self._create_and_save_settings(settings_data)

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
