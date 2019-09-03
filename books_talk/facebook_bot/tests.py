from unittest.mock import patch
import responses
from django.test import TestCase, override_settings
from facebook_bot.wrapper import get_user_data


class TestFacebookWebhook(TestCase):
    @override_settings(FB_VERIFY_TOKEN='_random_token_')
    def test_can_verify_token(self):
        response = self.client.get('/fb_webhook/', {
            'hub.mode': 'subscribe',
            'hub.challenge': '1089100139',
            'hub.verify_token': '_random_token_',
        })

        self.assertEqual(response.content, b'1089100139')

    def test_fail_to_verify_token_token_is_wrong(self):
        response = self.client.get('/fb_webhook/', {
            'hub.mode': 'subscribe',
            'hub.challenge': '1089100139',
            'hub.verify_token': '_wrong_token_',
        })
        self.assertEqual(response.status_code, 403)

    def test_can_process_messages(self):
        test_message = {
            "object": "page",
            'sender': {
                'id': '55512345'
            },
            "entry": [{
                "messaging": [{
                    "timestamp": 1567519931111,
                    "sender": {"id": 777},
                    "message": "TEST_MESSAGE"
                }]
            }]
        }

        with patch('facebook_bot.views.process_message') as process_message:
            response = self.client.post('/fb_webhook/', test_message, content_type='application/json',
                                        HTTP_X_Hub_Signature='sha1=ffa0bd5be2e096a6c618ee2b8b485e5f35e6bbb7')
        self.assertEqual(response.status_code, 200)
        process_message.assert_called_once()


class TestFacebookApiWrapper(TestCase):
    @responses.activate
    def test_can_get_access_to_information_about_user(self):
        responses.add(
            responses.GET, 'https://graph.facebook.com/5552649833',
            body='{"first_name": "Egor","id":"5559833"}',
            status=200, content_type='application/json'
        )

        response = get_user_data('5552649833')
        self.assertEqual(response['first_name'], 'Egor')
