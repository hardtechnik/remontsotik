from core.forms import TicketForm


def test_create_ticket(db, statuses, faker):
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
