from asyncio import gather
from unittest.mock import patch
from urllib.parse import urlencode, urljoin

from django.core import mail
from django.urls import reverse

import pytest
from core.models import Status, Ticket


async def fill_input(page, selector, value):
    field = await page.querySelector(selector)
    await field.type(value)


@pytest.fixture
def ticket(status_new):
    yield Ticket.objects.create(status=status_new, phone_number='9192223322')


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_create_ticket(page, absolute_url, statuses, settings):
    tickets = Ticket.objects.all()
    assert tickets.count() == 0

    settings.MANAGERS = [('Manager', 'manager@mail.com')]

    await page.goto(absolute_url('create_ticket'))

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

    assert len(mail.outbox) == 2
    mail_to_managers = mail.outbox[0]
    assert mail_to_managers.to == ['manager@mail.com']
    ticket_admin_url = urljoin(
        f'https://{settings.DOMAIN}',
        reverse('admin:core_ticket_change', args=(ticket.id,)),
    )
    assert ticket_admin_url in mail_to_managers.body

    mail_to_user = mail.outbox[1]
    assert mail_to_user.to == [email]
    assert mail_to_user.subject == f'Заявка №{ticket.number}'
    assert ticket.status.description in mail_to_user.body


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_search_ticket(page, absolute_url, ticket):
    await page.goto(absolute_url('create_ticket'))
    await fill_input(page, '#search', ticket.number)
    await gather(
        page.waitForNavigation(),
        page.click('.search-button'),
    )
    await gather(
        page.waitForFunction(
            f'document.querySelector("body").innerText'
            f'.includes("{ticket.number}")',
        ),
        page.waitForFunction(
            f'document.querySelector("body").innerText'
            f'.includes("{ticket.status.description}")',
        ),
    )


@pytest.mark.django_db
def test_ticket_detail_view(client, ticket):
    r = client.get(reverse('ticket_detail', kwargs={'number': ticket.number}))
    assert r.status_code == 200
    assert ticket.number in r.content.decode()


@pytest.mark.django_db
@patch('django.db.transaction.on_commit', lambda f: f())
def test_email_is_sent_on_status_change(status_new):
    assert len(mail.outbox) == 0

    ticket = Ticket.objects.create(
        status=status_new,
        phone_model='1234567890',
        email='customer@mail.com',
    )

    assert len(mail.outbox) == 1

    status_approved = Status.objects.create(name='approved', description='foo')
    ticket.status = status_approved
    ticket.save(update_fields=['status'])

    assert len(mail.outbox) == 2
    email = mail.outbox[1]
    assert 'foo' in email.body


@pytest.mark.django_db
def test_404_for_unknown_ticket(ticket, client):
    query_string = urlencode({'number': 42})
    r = client.get(f'{reverse("ticket_search")}?{query_string}')
    assert r.status_code == 404
