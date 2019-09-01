from django.test import TestCase, override_settings


class TestFacebookBot(TestCase):
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
