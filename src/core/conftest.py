import pytest
from django.core.management import call_command

from faker.factory import Factory as FakerFactory


_faker = FakerFactory.create()


@pytest.fixture
def faker():
    yield FakerFactory.create()


@pytest.fixture
def statuses():
    call_command('loaddata', 'statuses')
