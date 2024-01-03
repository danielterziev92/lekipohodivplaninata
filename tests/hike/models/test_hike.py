from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import DataError
from django.test import TestCase

from lekipohodivplaninata.hike.models import Hike, HikeLevel, HikeType


class TestHikeModel(TestCase):
    VALID_HIKE_TYPE_DATA = {
        'title': 'Test Type',
    }

    VALID_HIKE_LEVEL_DATA = {
        'title': 'Test Level',
    }

    VALID_HIKE_DATA = {
        'title': 'Test',
        'slug': 'test',
        'description': 'Test description',
        'duration': '10 minutes',
        'event_date': datetime.now(),
        'price': '1234.56',
        'main_picture': '',
    }

    def _create_and_save_hike(self, data):
        hike_type = HikeType.objects.create(**self.VALID_HIKE_TYPE_DATA)
        hike_level = HikeLevel.objects.create(**self.VALID_HIKE_LEVEL_DATA)

        hike = Hike.objects.create(type=hike_type, level=hike_level, **data)
        hike.full_clean()
        hike.save()
        return hike

    def test_create_hike__when_valid_data__expect_to_be_created(self):
        hike = self._create_and_save_hike(self.VALID_HIKE_DATA)
        self.assertEqual(Hike.objects.count(), 1)
        self.assertEqual(hike.title, self.VALID_HIKE_DATA['title'])

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
