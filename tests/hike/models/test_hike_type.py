from django.core.exceptions import ValidationError
from django.test import TestCase

from lekipohodivplaninata.hike.models import HikeType
from tests.valid_data_for_test import ValidDataForTest


class TestHikeTypeModel(TestCase, ValidDataForTest):
    INVALID_HIKE_TYPE_DATA = {
        'title': 't' * (HikeType.TITLE_MAX_LENGTH + 1)
    }

    @staticmethod
    def _create_and_save_hike_type(data):
        hike_type = HikeType(**data)
        hike_type.full_clean()
        hike_type.save()
        return hike_type

    def test_create__when_valida_data__expect_to_be_created(self):
        hike_type = self._create_and_save_hike_type(self.HIKE_TYPE_MODEL_DATA)
        self.assertEqual(self.HIKE_TYPE_MODEL_DATA['title'], hike_type.title)

    def test_create__when_invalid_data__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            self._create_and_save_hike_type(self.INVALID_HIKE_TYPE_DATA)

    def test_create__when_empty_data__expect_to_raise_exception(self):
        with self.assertRaises(ValidationError):
            self._create_and_save_hike_type({'title': None})
