from django.test import TestCase

from lekipohodivplaninata.hike.models import Hike


class TestHikeModel(TestCase):
    VALID_HIKE_DATA = {
        'title': 'Test',
        'slug': 'test',
        'type': None,
        'description': 'Test description',
        'level': None,
        'duration': '10 minutes',
        'event_date': '2020-01-10',
        'price': 10.10,
        'main_picture': '',
    }

    def _create_and_save_hike(self, data):
        hike = Hike.objects.create(**data)
        hike.full_clean()
        hike.save()
        return hike

    def test_create_hike__when_valid_data__expect_to_be_created(self):
        pass

    def test_create_hike__when_title_is_greater_with_one_character__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_title_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_slug_is_not_unique__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_slug_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_type_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_description_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_level_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_duration_is_greater_with_one_character__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_duration_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_event_date_is_before_today__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_event_date_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_price_is_greater_with_one_digits__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_price_is_more_with_one_decimal_place__expect_to_raise_exception(self):
        pass

    def test_create_hike__when_main_picture_is_null__expect_to_raise_exception(self):
        pass
