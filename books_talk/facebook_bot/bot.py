from goodreads_provider.wrapper import search_books
from .wrapper import send_message, get_user_data
from .models import FacebookSender


def hi(psid):
    first_name = get_user_data(psid)['first_name']
    send_message(psid, f'Hello {first_name}')


def choose_search_type(psid):
    send_message(psid, 'Do you want to search books by name or by ID (Goodreads ID)?',
                 {'search_title': 'Search by book title', 'search_id': 'Search by Goodreads ID'})


def search_books_and_let_user_choose(psid, text):
    books = search_books(text)[:5]
    if not books:
        send_message(psid, "Sorry, can't find anything, maybe let's try to search another book?")
        return False

    send_message(psid, 'Do you want to search books by name or by ID (Goodreads ID)?',
                 {'search_title': 'Search by book title', 'search_id': 'Search by Goodreads ID'})


def process_message(message):
    psid = message['sender']['id']
    reply_text = message['message']['text']
    quick_reply_payload = message['message'].get('quick_reply', {}).get('payload')
    sender_query = FacebookSender.objects.filter(psid=psid)

    if not sender_query.exists():
        hi(psid)
        choose_search_type(psid)
        FacebookSender.objects.create(psid=psid)
        return

    sender = sender_query.get()

    if quick_reply_payload in ['search_title', 'search_id']:
        if quick_reply_payload == 'search_title':
            sender.search_by = FacebookSender.SEARCH_BY_TITLE
            send_message(psid, 'Please send title of book which you are looking for.')
        else:
            sender.search_by = FacebookSender.SEARCH_BY_GOODREADS_ID
            send_message(psid, 'Please input Goodreads book id which you are looking for.')
        sender.save()
    if not sender.search_by:
        choose_search_type(psid)

    search_books_and_let_user_choose(psid, reply_text)