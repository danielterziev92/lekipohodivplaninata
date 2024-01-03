from datetime import datetime

from django.test import TestCase


class TestHikeAdditionalInfoModel(TestCase):
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

    VALID_HIKE_ADDITIONAL_INFO_DATA = {
        'event_venue': 'Test',
        'departure_time': '12:00:00',
        'departure_place': 'Test town',
    }

    def _create_and_save_hike_additional_info(self, data):
        pass

    def test_create_hike_additional_info__when_data_is_valid__expect_to_be_created(self):
        pass

    def test_create_hike_additional_info__when_hike_id_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike_additional_info__when_event_venue_is_with_one_more_character__expect_to_raise_exception(self):
        pass

    def test_create_hike_additional_info__when_event_venue_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike_additional_info__when_departure_time_is_null__expect_to_raise_exception(self):
        pass

    def test_create_hike_additional_info__when_departure_place_is_with_one_more_character__expect_to_raise_exception(
            self):
        pass

    def test_create_hike_additional_info__when_departure_place_is_null__expect_to_raise_exception(self):
        pass
