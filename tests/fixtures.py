import pytest
from django.contrib.auth.models import User

from django.test import Client, RequestFactory


@pytest.fixture
def client():
    return Client()


default_user_password = 'super-Secret123'

@pytest.fixture
def default_user():
    return User.objects.create_user(
        username='testUser', email='test@gmail.com', password=default_user_password
    )
