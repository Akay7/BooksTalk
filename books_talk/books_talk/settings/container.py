from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') and True or False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# API keys
# Goodreads
GOODREADS_KEY = os.environ.get('GOODREADS_KEY')
# IBM Watson
NATURAL_LANGUAGE_UNDERSTANDING_IAM_APIKEY = os.environ.get('NATURAL_LANGUAGE_UNDERSTANDING_IAM_APIKEY')
NATURAL_LANGUAGE_UNDERSTANDING_URL = os.environ.get('NATURAL_LANGUAGE_UNDERSTANDING_URL')
# Facebook
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
FB_APP_SECRET = os.environ.get('FB_APP_SECRET')
FB_PAGE_ACCESS_TOKEN = os.environ.get('FB_PAGE_ACCESS_TOKEN')
