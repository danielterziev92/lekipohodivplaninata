from django.db import DataError, IntegrityError
from django.test import TestCase

from lekipohodivplaninata.hike.models import HikeLevel


class TestHikeLevel(TestCase):
    VALID_HIKE_LEVEL_DATA = {
        'title': 'Test Hike Level',
    }

    def _create_and_save_hike_level(self, data):
        hike_level = HikeLevel.objects.create(**data)
        hike_level.full_clean()
        hike_level.save()
        return hike_level

    def test_create__when_valid_data__expect_to_be_created(self):
        self._create_and_save_hike_level(self.VALID_HIKE_LEVEL_DATA)
        self.assertEqual(HikeLevel.objects.count(), 1)

    def test_create__when_length_is_greater_with_one__expect_to_raise_exception(self):
        title = 'T' * (HikeLevel.TITLE_MAX_LENGTH + 1)
        with self.assertRaises(DataError):
            hike_level_data = {'title': title}
            self._create_and_save_hike_level(hike_level_data)

    def test_create__when_value_is_null__expect_to_raise_exception(self):
        title = None
        with self.assertRaises(IntegrityError):
            self._create_and_save_hike_level({'title': title})
