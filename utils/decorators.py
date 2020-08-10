from functools import wraps
from typing import Callable, Any

from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_required_message(
        func: Callable[..., HttpResponse],
        message: str = 'You need to log in first.') -> Callable:

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> HttpResponse:
        request = args[0]
        assert isinstance(request, HttpRequest)

        if not request.user.is_authenticated:
            messages.error(request, message)

        return login_required(func)(*args, **kwargs)

    return wrapper
