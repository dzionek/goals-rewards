from django.http import HttpResponse
from django.test import Client
from django.urls import reverse


def is_based_on_template(response: HttpResponse, template: str) -> bool:
    return template in (t.name for t in response.templates)


def check_login_required(client: Client, url_name: str) -> None:
    response = client.get(reverse(url_name), follow=True)
    assert response.status_code == 200
    assert 'You need to log in first' in response.content.decode()
