import factory
import pytest
from faker.factory import Factory as FakerFactory
from django.contrib.auth import get_user_model
from pytest_factoryboy import register


_faker = FakerFactory.create()


@pytest.fixture
def faker():
    yield FakerFactory.create()


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = _faker.user_name()
    is_active = True

    class Meta:
        model = get_user_model()
