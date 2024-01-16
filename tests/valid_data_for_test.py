from datetime import datetime


class ValidDataForTest:
    USER_MODEL_DATA = {
        'email': 'test@example.com',
        'password': 'Password123.'
    }

    BASE_MODEL_DATA = {
        'first_name': 'Test',
        'last_name': 'Tester',
        'phone_number': '+359888998899'
    }

    GUIDE_MODEL_DATA = {
        'avatar': 'https://res.cloudinary.com/dujto2hys/image/upload/v1691335446/user-avatar_cyynjj_hjdus6.png',
        'date_of_birth': '1970-01-01',
        'description': 'Test description',
        'certificate': 'https://res.cloudinary.com/dujto2hys/image/upload/v1704290832/certificate.avif',
    }

    HIKE_TYPE_MODEL_DATA = {
        'title': 'Test Type',
    }

    HIKE_LEVEL_MODEL_DATA = {
        'title': 'Test Level',
    }

    HIKE_MODEL_DATA = {
        'title': 'Test',
        'slug': 'test',
        'description': 'Test description',
        'duration': '10 minutes',
        'event_date': datetime.now(),
        'price': '1234.56',
        'main_picture': '',
    }

    HIKE_ADDITIONAL_INFO_MODEL_DATA = {
        'event_venue': 'Test',
        'departure_time': '12:00:00',
        'departure_place': 'Test town',
    }
