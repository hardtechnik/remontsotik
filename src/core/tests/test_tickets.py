from asyncio import gather
from urllib.parse import urljoin

from django.core import mail

import pytest
from django.urls import reverse

from core.models import Ticket

pytestmark = pytest.mark.asyncio


async def fill_input(page, selector, value):
    field = await page.querySelector(selector)
    await field.type(value)


@pytest.mark.django_db
async def test_create_ticket(page, absolute_url, statuses, settings):
    tickets = Ticket.objects.all()
    assert tickets.count() == 0

    settings.MANAGERS = [('Manager', 'manager@mail.com')]

    await page.goto(absolute_url('index'))

    name = 'Рустам'
    phone_model = 'Xiaomi Redmi 5 Plus'
    malfunction = 'Треснул экран'
    phone_number = '9876543210'
    email = 'customer@mail.com'
    address = 'г.Казань'

    await fill_input(page, '#name', name)
    await fill_input(page, '#phone-model', phone_model)
    await fill_input(page, '#malfunction', malfunction)
    await fill_input(page, '#phone-number', phone_number)
    await fill_input(page, '#email', email)
    await fill_input(page, '#address', address)
    await gather(
        page.waitForNavigation(),
        page.click('#submit'),
    )

    ticket = tickets.get()
    await page.waitForFunction(
        f'document.querySelector("body").innerText.includes("{ticket.number}")',
    )

    assert ticket.number
    assert ticket.status.name == 'Новая'
    assert ticket.name == name
    assert ticket.phone_model == phone_model
    assert ticket.malfunction == malfunction
    assert ticket.phone_number == phone_number
    assert ticket.email == email
    assert ticket.address == address

    sent_email = mail.outbox[0]
    assert sent_email.to == ['manager@mail.com']
    ticket_admin_url = urljoin(
        f'https://{settings.DOMAIN}',
        reverse('admin:core_ticket_change', args=(ticket.id,)),
    )
    assert ticket_admin_url in sent_email.body
