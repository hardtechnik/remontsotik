import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['rkashapov.tk']

STATIC_URL = 'https://storage.yandexcloud.net/remontsotik/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
    }
}

ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv('SENDGRID_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@remontsotik.ru"
SERVER_EMAIL = "server@remontsotik.ru"

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
PRIVATE_BUCKET = os.getenv('PRIVATE_BUCKET')

MANAGERS = [
    'hardtechnik91@gmail.com',
    'n.murtazin22@gmail.com',
]

ADMINS = [
    'hardtechnik91@gmail.com',
]
