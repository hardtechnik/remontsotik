import base64
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment


def inline(src, mime):
    with open(finders.find(src), 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    return f'data:{mime};base64,{content}'


def absolute_url(url):
    scheme = 'http://' if 'localhost' in settings.DOMAIN else 'https://'
    return urljoin(f'{scheme}{settings.DOMAIN}', url)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'inline': inline,
        'absolute_url': absolute_url,
        'url': reverse,
        'DEBUG': settings.DEBUG,
    })
    return env
