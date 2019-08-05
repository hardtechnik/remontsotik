from asyncio import gather

import pytest

from core.models import Ticket

pytestmark = pytest.mark.asyncio


async def fill_input(page, selector, value):
    field = await page.querySelector(selector)
    await field.type(value)


async def test_create_ticket(db, page, view_url, statuses):
    tickets = Ticket.objects.all()
    assert tickets.count() == 0
    await page.goto(view_url('index'))

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
