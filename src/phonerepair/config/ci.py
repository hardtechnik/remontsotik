from .base import *

CI = True
DOMAIN = 'test.server'
ALLOWED_HOSTS = [DOMAIN]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '::memory::',
    }
}
