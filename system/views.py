from django.shortcuts import render

from utils.decorators import login_required_message

@login_required_message
def home(request):
    username = request.user.username
    return render(request, 'system/home.html', {'username': username})
