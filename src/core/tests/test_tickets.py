from core.forms import TicketForm
from core.models import Ticket


def test_create_ticket(db, faker):
    form = TicketForm(
        data={
            'phone_model': faker.word(),
            'malfunction': faker.sentence(),
            'email': faker.email(),
            'phone_number': faker.phone_number(),
            'address': faker.address(),
        },
    )
    assert form.is_valid()

    ticket = form.save()
    assert ticket.id
    assert len(ticket.number) == 6
    assert ticket.created
    assert ticket.status == Ticket.STATUS_CREATED
