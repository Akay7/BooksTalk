import xml.etree.ElementTree as ET
import requests
from django.conf import settings

GOODREADS_KEY = getattr(settings, 'GOODREADS_KEY')


def search_books(phrase):
    params = {
        'q': phrase,
        'key': GOODREADS_KEY,
    }
    response = requests.get('https://www.11goodreads.com/search/index.xml', params)
    root_el = ET.fromstring(response.content)

    books = []
    for book_el in root_el.findall('search//work//best_book'):
        book = {
            'title': book_el.find('title').text,
            'author': [name_el.text for name_el in book_el.findall('author//name')],
            'image_url': book_el.find('image_url').text,
        }
        books.append(book)
    return books
