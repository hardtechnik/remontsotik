import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

DOMAIN = os.getenv('DOMAIN')
ALLOWED_HOSTS = [DOMAIN]

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

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_CACHE_DB = 1

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            '%s:%s' % (REDIS_HOST, REDIS_PORT),
            ],
        'OPTIONS': {
            'DB': REDIS_CACHE_DB,
            'PASSWORD': '',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 10,
                'timeout': 20,
            },
        },
    },
}

ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv('SENDGRID_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@remontsotik.ru"
SERVER_EMAIL = "Ремонт Сотик <server@remontsotik.ru>"
EMAIL_SUBJECT_PREFIX = ''

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
PRIVATE_BUCKET = os.getenv('PRIVATE_BUCKET')

MANAGERS = [
    ('Рустам', 'hardtechnik91@gmail.com'),
    ('Нияз', 'n.murtazin22@gmail.com'),
]

CSRF_COOKIE_SECURE = True

sentry_sdk.init(
    dsn="https://372dfc07100b440589ff044789f2a637@sentry.io/1526451",
    integrations=[DjangoIntegration()]
)
