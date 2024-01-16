from datetime import datetime

from django.db import IntegrityError, DataError
from django.test import TestCase

from lekipohodivplaninata.hike.models import HikeLevel, HikeType, Hike, HikeAdditionalInfo
from tests.valid_data_for_test import ValidDataForTest


class HikeAdditionalInfoModelForTest(TestCase, ValidDataForTest):
    def _create_and_save_hike_additional_info(self, data):
        hike_level = HikeLevel.objects.create(**self.HIKE_LEVEL_MODEL_DATA)
        hike_type = HikeType.objects.create(**self.HIKE_TYPE_MODEL_DATA)
        hike = Hike.objects.create(**self.HIKE_MODEL_DATA, level=hike_level, type=hike_type)

        hike_additional_info = {'hike_id': hike, **data}

        hike_additional_info = HikeAdditionalInfo.objects.create(**hike_additional_info)
        hike_additional_info.full_clean()
        hike_additional_info.save()
        return hike_additional_info

    def test_create_hike_additional_info__when_data_is_valid__expect_to_be_created(self):
        hike_additional_info = self._create_and_save_hike_additional_info(self.HIKE_ADDITIONAL_INFO_MODEL_DATA)
        self.assertEqual(HikeAdditionalInfo.objects.count(), 1)
        self.assertEqual(hike_additional_info.event_venue, self.HIKE_ADDITIONAL_INFO_MODEL_DATA['event_venue'])

    def test_create_hike_additional_info__when_hike_id_is_null__expect_to_raise_exception(self):
        with self.assertRaises(IntegrityError):
            self._create_and_save_hike_additional_info({**self.HIKE_ADDITIONAL_INFO_MODEL_DATA, 'hike_id': None})

    def test_create_hike_additional_info__when_event_venue_is_with_one_more_character__expect_to_raise_exception(self):
        event_venue = 't' * (HikeAdditionalInfo.EVENT_VENUE_MAX_LENGTH + 1)
        with self.assertRaises(DataError):
            hike_additional_info_data = {**self.HIKE_ADDITIONAL_INFO_MODEL_DATA, 'event_venue': event_venue}
            self._create_and_save_hike_additional_info(hike_additional_info_data)

    def test_create_hike_additional_info__when_event_venue_is_null__expect_to_raise_exception(self):
        with self.assertRaises(IntegrityError):
            self._create_and_save_hike_additional_info({**self.HIKE_ADDITIONAL_INFO_MODEL_DATA, 'event_venue': None})

    def test_create_hike_additional_info__when_departure_time_is_null__expect_to_raise_exception(self):
        with self.assertRaises(IntegrityError):
            self._create_and_save_hike_additional_info({**self.HIKE_ADDITIONAL_INFO_MODEL_DATA, 'departure_time': None})

    def test_create_hike_additional_info__when_departure_place_is_with_one_more_character__expect_to_raise_exception(
            self):
        departure_place = 't' * (HikeAdditionalInfo.DEPARTURE_PLACE_MAX_LENGTH + 1)
        with self.assertRaises(DataError):
            hike_additional_info_data = {**self.HIKE_ADDITIONAL_INFO_MODEL_DATA, 'departure_place': departure_place}
            self._create_and_save_hike_additional_info(hike_additional_info_data)

    def test_create_hike_additional_info__when_departure_place_is_null__expect_to_raise_exception(self):
        with self.assertRaises(IntegrityError):
            self._create_and_save_hike_additional_info(
                {**self.HIKE_ADDITIONAL_INFO_MODEL_DATA, 'departure_place': None})
