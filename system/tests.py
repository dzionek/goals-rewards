import pytest

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from tests.fixtures import client, default_user

@pytest.mark.django_db
class TestRoutes:
    def test_home(self, client: Client, default_user: User) -> None:
        response = client.get(reverse('system_home'), follow=True)
        assert response.status_code == 200
        assert 'You need to log in first' in response.content.decode()

        client.force_login(default_user)

        response = client.get(reverse('system_home'))
        assert response.status_code == 200
        assert 'Welcome in Goals & Rewards application' in response.content.decode()
