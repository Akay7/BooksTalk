import requests
from django.conf import settings


def get_user_data(psid, fields=('first_name',)):
    page_access_token = getattr(settings, 'FB_PAGE_ACCESS_TOKEN')
    params = {
        'fields': fields,
        'access_token': page_access_token
    }
    url = f"https://graph.facebook.com/{psid}"
    response = requests.get(url, params)
    return response.json()


def send_response_text_message(psid, text):
    message = {
        "text": text
    }
    return send_response_message(psid, message)


def send_response_image_message(psid, image_url):
    message = {
        "attachment": {
          "type": "image",
          "payload": {
            "url": image_url,
            "is_reusable": 'true'
          }
        }
    }
    return send_response_message(psid, message)


def send_response_message(psid, message):
    payload = {
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': psid
        },
        "message": message
    }

    page_access_token = getattr(settings, 'FB_PAGE_ACCESS_TOKEN')
    url = f'https://graph.facebook.com/v4.0/me/messages?access_token={page_access_token}'
    response = requests.post(url, json=payload)
    return response.json()
