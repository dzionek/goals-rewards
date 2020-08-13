from typing import Union, Type

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import AddDirectRewardForm, AddPointRewardForm


AddRewardForm = Union[Type[AddDirectRewardForm], Type[AddPointRewardForm]]


def add_reward(request: HttpRequest, add_reward_form: AddRewardForm,
               form_title: str) -> HttpResponse:

    if request.method == 'POST':
        form = add_reward_form(request.POST)
        if form.is_valid():
            checked_form = form.save(commit=False)
            checked_form.user = request.user
            checked_form.save()
            messages.success(request, 'The reward was successfully added!')
            return redirect(reverse('system_home'))
    else:
        form = add_reward_form()
    context = dict(form=form, form_title=form_title)
    return render(request, 'system/form.html', context)
