from os import path
from django.test import TestCase
from unittest.mock import patch

from ..wrapper import search_books, book_reviews


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

    def test_failed_search_must_return_empty_books(self):
        with patch('goodreads_provider.wrapper.requests.get',
                   side_effect=load_mocked_requests_from_file('response_search_empty.xml')) as mock_get:
            books = search_books('cant find anything')

        self.assertEqual(len(books), 0)

    def test_get_review_to_selected_book(self):
        with patch('goodreads_provider.wrapper.requests.get',
                   side_effect=load_mocked_requests_from_file('book_reviews.xml')) as mock_get:
            reviews = book_reviews(24583)

        self.assertEqual(len(reviews), 30)
        self.assertEqual(reviews[0], {
            'body': "It's odd that I didn't like this book because I am usually such a big fan of Mark Twain. I loved his book The Prince and the Pauper, and acknowledge that Tom Sawyer is very well-written. However, I thought the characters were idiots. All they did all day long was boast about who could smoke a pip..."
        })