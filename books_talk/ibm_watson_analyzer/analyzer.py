import requests
from django.conf import settings

NATURAL_LANGUAGE_UNDERSTANDING_IAM_APIKEY = getattr(settings, 'NATURAL_LANGUAGE_UNDERSTANDING_IAM_APIKEY')
NATURAL_LANGUAGE_UNDERSTANDING_URL = getattr(settings, 'NATURAL_LANGUAGE_UNDERSTANDING_URL')


def analyze_sentiments(text):
    payload = {
        "text": text,
        "features": {
            "sentiment": {}
        }
    }
    url = f'{NATURAL_LANGUAGE_UNDERSTANDING_URL}/v1/analyze?version=2019-07-12'
    response = requests.post(url, json=payload, auth=('apikey', NATURAL_LANGUAGE_UNDERSTANDING_IAM_APIKEY))
    return response.json()['sentiment']['document']['score']
