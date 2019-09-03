import xml.etree.ElementTree as ET
import requests
from django.conf import settings

GOODREADS_KEY = getattr(settings, 'GOODREADS_KEY')


def search_books(phrase):
    params = {
        'q': phrase,
        'search[field]': 'title',
        'key': GOODREADS_KEY,
    }
    response = requests.get('https://www.goodreads.com/search/index.xml', params)
    root_el = ET.fromstring(response.content)

    books = []
    for book_el in root_el.findall('search//work//best_book'):
        book = {
            'id': int(book_el.find('id').text),
            'title': book_el.find('title').text,
            'author': [name_el.text for name_el in book_el.findall('author//name')],
            'image_url': book_el.find('image_url').text,
        }
        books.append(book)
    return books


def get_book(goodreads_id):
    params = {
        'id': goodreads_id,
        'key': GOODREADS_KEY,
    }
    response = requests.get('https://www.goodreads.com/book/show.xml', params)

    root_el = ET.fromstring(response.content)

    if root_el.find('book') is None:
        return None

    book = {
        'id': int(root_el.find('book//id').text),
        'title': root_el.find('book//title').text,
        'author': [name_el.text for name_el in root_el.findall("book//authors//author[role='']//name")],
        'image_url': root_el.find('book//image_url').text,
    }

    return book


def book_reviews(goodreads_id):
    params = {
        'text_only': 'true',
        'sort': 'newest',
        'language_code': 'en',
        'key': GOODREADS_KEY,
    }

    url = f"https://www.goodreads.com/book/reviews/{goodreads_id}"
    response = requests.get(url, params)
    root_el = ET.fromstring(response.content)

    reviews = []
    for review_el in root_el.findall('reviews//review'):
        review = {
            'body': review_el.find('body').text.strip()
        }
        reviews.append(review)

    return reviews
