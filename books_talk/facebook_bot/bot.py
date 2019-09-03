from goodreads_provider.wrapper import search_books
from .wrapper import send_response_text_message, send_response_image_message, send_response_message, get_user_data
from .models import FacebookSender


class BotReply:
    ACTION_SELECT_SEARCH_TYPE = 'select_search_type'
    ACTION_SELECT_BOOK = 'select_book'

    REPLY_SEARCH_BY_TITLE = {
        'title': 'Search by book title',
        'content_type': 'text',
        'payload': f'{ACTION_SELECT_SEARCH_TYPE}={FacebookSender.SEARCH_BY_TITLE}',
    }
    REPLY_SEARCH_BY_GOODREADS_ID = {
        'title': 'Search by Goodreads ID',
        'content_type': 'text',
        'payload': f'{ACTION_SELECT_SEARCH_TYPE}={FacebookSender.SEARCH_BY_GOODREADS_ID}',
    }

    def __init__(self, message):
        self.psid = message['sender']['id']
        self.reply_text = message['message']['text']
        self.sender_reply = message['message'].get('quick_reply', {}).get('payload')
        self.sender = FacebookSender.objects.filter(psid=self.psid).first()
        self.is_first_message = not self.sender and True

    def hint_hi(self):
        first_name = get_user_data(self.psid)['first_name']
        send_response_text_message(self.psid, f'Hello {first_name}')

    def hint_choose_search_type(self):
        message = {
            'text': 'Do you want to search books by name or by ID (Goodreads ID)?',
            'quick_replies': [BotReply.REPLY_SEARCH_BY_TITLE, BotReply.REPLY_SEARCH_BY_TITLE]
        }
        send_response_message(self.psid, message)

    def create_sender(self):
        self.sender = FacebookSender.objects.create(psid=self.psid)
        return self.sender

    def action_choose_search_type(self, select):
        self.sender.search_by = select
        if self.sender.search_by == FacebookSender.SEARCH_BY_TITLE:
            send_response_message(self.psid, 'Please send title of book which you are looking for.')
        else:
            send_response_message(self.psid, 'Please input Goodreads book id which you are looking for.')
        self.sender.save()

    def search_books_and_let_user_choose(self, text):
        books = search_books(text)[:5]
        if not books:
            send_response_text_message(self.psid, "Sorry, can't find anything, maybe let's try to search another book?")
            return False

        send_response_text_message(self.psid, 'Here what we find:')
        replies = []
        for number, book in enumerate(books, 1):
            send_response_text_message(
                self.psid, "{number}.{book_title} - {author}".format(
                    number=number, book_title=book['title'], author=','.join(book['author'])
                )
            )
            send_response_image_message(self.psid, book['image_url'])
            replies.append({
                'title': str(number),
                'content_type': 'text',
                'payload': f"{BotReply.ACTION_SELECT_BOOK}={book['id']}"
            })

        if self.sender.search_by == FacebookSender.SEARCH_BY_TITLE:
            replies.append(BotReply.REPLY_SEARCH_BY_GOODREADS_ID)
        else:
            replies.append(BotReply.REPLY_SEARCH_BY_TITLE)

        send_response_message(self.psid, {
            'text': 'You can choose book or change type of searching:',
            'quick_replies': replies,
        })

    def action_select_book(self, book_id):
        send_response_text_message(self.psid, 'You choose book' + book_id)
        # fixME

    def process_action(self):
        action_mapping = {
            BotReply.ACTION_SELECT_SEARCH_TYPE: self.action_choose_search_type,
            BotReply.ACTION_SELECT_BOOK: self.action_select_book
        }
        if self.sender_reply:
            reply_action, reply_select = self.sender_reply.split('=')

            action = action_mapping[reply_action]
            action(reply_select)
        else:
            self.search_books_and_let_user_choose(self.reply_text)


def process_message(message):
    bot_reply = BotReply(message)

    if bot_reply.is_first_message:
        bot_reply.hint_hi()
        bot_reply.hint_choose_search_type()
        bot_reply.create_sender()
        return

    bot_reply.process_action()
