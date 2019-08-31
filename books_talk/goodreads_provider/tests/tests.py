from os import path
from django.test import TestCase
from unittest.mock import Mock, patch, PropertyMock

from ..wrapper import search_books


def load_mocked_requests_from_file(filename):
    def mocked_requests(*args, **kwargs):
        class MockResponse:
            def __init__(self, filename):
                file = open(path.join(path.dirname(__file__), filename), 'rb')
                self.content = file.read()

        return MockResponse(filename)
    return mocked_requests


class TestWrapperMethods(TestCase):
    def test_search_books_return_dict_entities_with_information_about_book(self):
        with patch('goodreads_provider.wrapper.requests.get',
                   side_effect=load_mocked_requests_from_file('response_search.xml')) as mock_get:

            books = search_books('mark twain')

        self.assertEqual(len(books), 20)
        self.assertEqual(books[0], {
            'title': 'The Adventures of Huckleberry Finn',
            'author': ['Mark Twain'],
            'image_url': 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1546096879l/2956._SX98_.jpg'
        })

