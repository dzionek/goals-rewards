from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from utils.decorators import login_required_message

@login_required_message
def home(request: HttpRequest) -> HttpResponse:
    username = request.user.username
    return render(request, 'system/home.html', {'username': username})
