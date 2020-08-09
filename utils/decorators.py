from functools import wraps

from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_required_message(func, message='You need to log in first.'):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if not isinstance(request, HttpRequest):
            raise TypeError('First arg of the function decorated by login_required_message must be a request.')

        if not request.user.is_authenticated:
            messages.error(request, message)

        return login_required(func)(*args, **kwargs)

    return wrapper
