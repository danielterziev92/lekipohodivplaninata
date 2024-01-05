from django.test import TestCase

from lekipohodivplaninata.base.models import SocialMedia


class TestSocialMediaModel(TestCase):
    VALID_SOCIAL_MEDIA_DATA = {
        'name': 'Test',
        'url': 'https://example.com',
        'fontawesome_icon': 'fa-test',
        'icon_color': 'ffffff'
    }

    def _create_and_save_social_media(self, data):
        social_media = SocialMedia.objects.create(**data)
        social_media.full_clean()
        social_media.save()
        return social_media

    def test_create_social_media__when_valid_data__expect_to_be_created(self):
        social_media = self._create_and_save_social_media(self.VALID_SOCIAL_MEDIA_DATA)

        self.assertEqual(SocialMedia.objects.count(), 1)
        self.assertEqual(social_media.name, self.VALID_SOCIAL_MEDIA_DATA['name'])

    def test_create_social_media__when_name_is_with_one_more_character_more__expect_to_raise_exception(self):
        pass

    def test_create_social_media__when_name_is_null__expect_to_raise_exception(self):
        pass

    def test_create_social_media__when_url_is_empty__expect_to_raise_exception(self):
        pass

    def test_create_social_media__when_fontawesome_icon_is_with_one_more_character_more__expect_to_raise_exception(
            self):
        pass

    def test_create_social_media__when_fontawesome_icon_is_null__expect_to_raise_exception(self):
        pass

    def test_create_social_media__when_icon_color_is_with_one_more_character_more__expect_to_raise_exception(self):
        pass

    def test_create_social_media__when_icon_color_is_null__expect_to_raise_exception(self):
        pass
