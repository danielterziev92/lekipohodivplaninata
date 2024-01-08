from django.test import TestCase

from lekipohodivplaninata.api_app.models import Subscribe


class TestSubscribeModel(TestCase):
    VALID_SUBSCRIBE_DATA = {
        'email': 'email@example.com',
        'is_active': True,
        'slug_to_unsubscribe': 'kvUt+d84hMcN@"}2T-:DL9',
    }

    def _create_and_save_subscribe(self, data):
        subscribe = Subscribe.objects.create(**data)
        subscribe.full_clean()
        subscribe.save()
        return subscribe

    def test_create__when_valid_data__expect_to_be_created(self):
        pass

    def test_create__when_email_is_not_unique__expect_to_raise_exception(self):
        pass

    def test_create__when_email_is_null__expect_to_raise_exception(self):
        pass

    def test_create__when_slug_is_not_unique__expect_to_raise_exception(self):
        pass

    def test_create__when_slug_is_null__expect_to_be_created(self):
        pass
