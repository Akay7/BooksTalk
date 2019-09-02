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
