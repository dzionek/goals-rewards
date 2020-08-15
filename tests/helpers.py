from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse


def is_based_on_template(response: HttpResponse, template: str) -> bool:
    return template in (t.name for t in response.templates)


def check_login_required(client: Client, url_name: str) -> None:
    response = client.get(reverse(url_name), follow=True)
    assert response.status_code == 200
    assert 'You need to log in first' in response.content.decode()


def check_view_set_admin_restricted(client: Client, url: str, non_admin: User,
                                    admin: User) -> HttpResponse:
    response = client.get(url)
    assert response.status_code == 403

    client.force_login(non_admin)
    response = client.get(url)
    assert response.status_code == 403

    client.logout()
    client.force_login(admin)
    response = client.get(url)
    assert response.status_code == 200

    return response


def check_view_set_user_restricted(client: Client, url: str,
                                   user: User) -> HttpResponse:
    response = client.get(url)
    assert response.status_code == 403

    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

    return response
