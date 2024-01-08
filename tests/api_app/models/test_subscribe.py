from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from lekipohodivplaninata.api_app.models import Subscribe


class TestSubscribeModel(TestCase):
    VALID_SUBSCRIBE_DATA = {
        'email': 'email@example.com',
        'is_active': True,
        'slug_to_unsubscribe': 'test-slug',
    }

    def _create_and_save_subscribe(self, data):
        subscribe = Subscribe.objects.create(**data)
        subscribe.full_clean()
        subscribe.save()
        return subscribe

    @patch('lekipohodivplaninata.core.tasks.send_email_to_subscriber.delay')
    def test_create__when_valid_data__expect_to_be_created(self, mock_send_email):
        subscribe = self._create_and_save_subscribe(self.VALID_SUBSCRIBE_DATA)

        self.assertEqual(Subscribe.objects.count(), 1)
        self.assertEqual(subscribe.email, self.VALID_SUBSCRIBE_DATA['email'])

        # Test that subscribed_at is automatically set
        self.assertIsNotNone(subscribe.subscribed_at)

        mock_send_email.assert_called_once_with(email=subscribe.email)

    @patch('lekipohodivplaninata.core.tasks.send_email_to_subscriber.delay')
    def test_create__when_email_is_not_unique__expect_to_raise_exception(self, mock_send_email):
        subscribe = self._create_and_save_subscribe(self.VALID_SUBSCRIBE_DATA)

        mock_send_email.assert_called_once_with(email=subscribe.email)

        with self.assertRaises(IntegrityError):
            subscribe_data = {**self.VALID_SUBSCRIBE_DATA, 'slug_to_unsubscribe': 'test-slug-2'}
            self._create_and_save_subscribe(subscribe_data)

    def test_create__when_email_is_null__expect_to_raise_exception(self):
        pass

    @patch('lekipohodivplaninata.core.tasks.send_email_to_subscriber.delay')
    def test_create__when_slug_is_not_unique__expect_to_raise_exception(self, mock_send_email):
        subscribe = self._create_and_save_subscribe(self.VALID_SUBSCRIBE_DATA)

        mock_send_email.assert_called_once_with(email=subscribe.email)

        with self.assertRaises(IntegrityError):
            subscribe_data = {**self.VALID_SUBSCRIBE_DATA, 'email': 'email2@example.com'}
            self._create_and_save_subscribe(subscribe_data)

    def test_create__when_slug_is_null__expect_to_be_created(self):
        pass
