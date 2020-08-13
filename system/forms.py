from django import forms

from .models import PointReward, DirectReward, Goal


class DateInput(forms.DateInput):
    input_type = 'date'


class AddPointRewardForm(forms.ModelForm):

    class Meta:
        model = PointReward
        exclude = ['user']


class AddDirectRewardForm(forms.ModelForm):
    class Meta:
        model = DirectReward
        exclude = ['user']


class AddGoalForm(forms.ModelForm):
    finish_date = forms.DateField(widget=DateInput, required=False)

    class Meta:
        model = Goal
        exclude = ['user']
