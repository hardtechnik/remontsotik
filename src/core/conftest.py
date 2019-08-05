import os
from urllib.parse import urljoin

import pytest
from django.core.management import call_command
from django.conf import settings
from django.urls import reverse

import pyppeteer
from faker.factory import Factory as FakerFactory
from pytest_django.live_server_helper import LiveServer

_faker = FakerFactory.create()


@pytest.fixture
def faker():
    yield FakerFactory.create()


@pytest.fixture
def statuses():
    call_command('loaddata', 'statuses')


@pytest.fixture
async def browser():
    if settings.CI:
        b = await pyppeteer.connect({
            'browserWSEndpoint': 'ws://browser:3000',
        })
    else:
        b = await pyppeteer.launch({'headless': False})
    yield b
    await b.disconnect()


@pytest.fixture
async def page(request, browser, live_server):
    p = await browser.newPage()

    yield p

    if request.node.rep_call.failed:
        os.makedirs('screenshots', exist_ok=True)
        await p.screenshot({
            'path': f'screenshots/{request.node.nodeid.replace("/", ".")}.jpg',
        })

    await p.close()


if settings.CI:
    @pytest.fixture(scope='session')
    def live_server(request):
        server = LiveServer('0.0.0.0:43923')
        request.addfinalizer(server.stop)
        yield server


@pytest.fixture
def view_url(live_server):
    def f(view_name):
        view_url = view_name
        if not view_name.startswith('/'):
            view_url = reverse(view_name)
        if settings.CI:
            host = 'http://test.server:43923'
        else:
            host = live_server.url
        return urljoin(host, view_url)
    return f


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
