import base64

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment


def inline(src, mime):
    with open(finders.find(src), 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    return f'data:{mime};base64,{content}'


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'inline': inline,
        'url': reverse,
    })
    return env
