from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') and True or False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# API keys
GOODREADS_KEY = os.environ.get('GOODREADS_KEY')
