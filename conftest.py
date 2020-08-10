import pytest

from django.contrib.auth.models import User
from django.test import Client

from tests.constants import default_user_password


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def default_user() -> User:
    return User.objects.create_user(
        username='testUser', email='test@gmail.com',
        password=default_user_password
    )
