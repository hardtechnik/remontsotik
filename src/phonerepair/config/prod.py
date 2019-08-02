import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['rkashapov.tk']

STATIC_URL = 'https://storage.yandexcloud.net/remontsotik/static/'
