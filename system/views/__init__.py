from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from utils.decorators import login_required_message

from ..forms import AddPointRewardForm, AddDirectRewardForm, AddGoalForm
from .helpers import add_reward


@login_required_message
def home(request: HttpRequest) -> HttpResponse:
    username = request.user.username
    return render(request, 'system/home.html', {'username': username})


@login_required_message
def add_point_reward(request: HttpRequest) -> HttpResponse:
    return add_reward(request, AddPointRewardForm, 'Add Point Reward')


@login_required_message
def add_direct_reward(request: HttpRequest) -> HttpResponse:
    return add_reward(request, AddDirectRewardForm, 'Add Direct Reward')


@login_required_message
def add_goal(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AddGoalForm(request.POST)
        if form.is_valid():
            checked_form = form.save(commit=False)
            checked_form.user = request.user
            checked_form.save()
            messages.success(request, 'The goal was successfully added!')
            return redirect(reverse('system_home'))
    else:
        form = AddGoalForm()

    return render(request, 'system/add-goal.html', {'form': form})
