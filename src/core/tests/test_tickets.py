from faker.factory import Factory

from core.models import Ticket


faker = Factory.create()


def test_create_ticket(db, user_factory, phone_factory,
                       malfunction_factory):
    user = user_factory.create()
    ticket = Ticket(
        user=user,
        phone_model=phone_factory.create(),
        malfunction=malfunction_factory.create(),
        phone_number=faker.phone_number(),
    )
    ticket.save()
    assert ticket.id
