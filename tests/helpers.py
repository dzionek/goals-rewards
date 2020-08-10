from django.http import HttpResponse


def is_based_on_template(response: HttpResponse, template: str) -> bool:
    return template in (t.name for t in response.templates)
