from os import path
from django.test import TestCase
from unittest.mock import patch

from ..analyzer import analyze_sentiments


def load_mocked_requests_from_file(filename):
    def mocked_requests(*args, **kwargs):
        class MockResponse:
            def __init__(self, filename):
                file = open(path.join(path.dirname(__file__), filename), 'rb')
                self.content = file.read()

        return MockResponse(filename)
    return mocked_requests


class TestAnalyzeSentiments(TestCase):
    def test_can_analyze_sentiments_and_give_positive_score(self):
        with patch('goodreads_provider.wrapper.requests.get',
                   side_effect=load_mocked_requests_from_file('apocalypse_today_sentence_analyze.json')) as mock_get:
            score = analyze_sentiments(
                'Napalm, son. Nothing else in the world smells like that.'
                'I love the smell of napalm in the morning. '
                'You know, one time we had a hill bombed, for 12 hours. '
                'When it was all over, I walked up. '
                "We didn’t find one of 'em, not one stinkin' dink body. "
                'The smell, you know that gasoline smell, the whole hill. '
                'Smelled like… victory.'
                'Someday this war’s gonna end…'
            )
        self.assertEqual(score, 0.294953)

    def test_can_analyze_sentiments_and_give_negative_score(self):
        with patch('goodreads_provider.wrapper.requests.get',
                   side_effect=load_mocked_requests_from_file('fight_club_sentence_analyze.json')) as mock_get:
            score = analyze_sentiments(
                'Listen up maggots! You are not special! You are not a beautiful or unique snowflake! '
                'You are the same decaying organic matter as everything else! We are the all singing, '
                'all dancing crap of the world! We are all part of the same compost keep.'
            )
        self.assertAlmostEqual(score, -0.539684)
