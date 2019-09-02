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


def send_message(psid, text, quick_replies=None):
    page_access_token = getattr(settings, 'FB_PAGE_ACCESS_TOKEN')
    payload = {
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': psid
        },
        "message": {
            "text": text
        }
    }
    if quick_replies:
        payload['message']['quick_replies'] = []
        for reply_payload, reply_title in quick_replies.items():
            payload['message']['quick_replies'].append({
                "content_type": "text",
                "title": reply_title,
                "payload": reply_payload,
            })

    url = f'https://graph.facebook.com/v4.0/me/messages?access_token={page_access_token}'
    response = requests.post(url, json=payload)
    return response.json()
