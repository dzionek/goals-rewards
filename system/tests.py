import pytest
from datetime import datetime
import pytz

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from .models import DirectReward, PointReward, UserPoint, Goal


@pytest.mark.django_db
class TestRoutes:
    def test_home(self, client: Client, default_user: User) -> None:
        response = client.get(reverse('system_home'), follow=True)
        assert response.status_code == 200
        assert 'You need to log in first' in response.content.decode()

        client.force_login(default_user)

        response = client.get(reverse('system_home'))
        assert response.status_code == 200
        assert 'Welcome in ' in response.content.decode()


@pytest.mark.django_db
class TestModels:
    def test_user_point(self, default_user: User) -> None:
        user_point = UserPoint.objects.get(pk=1)
        assert str(user_point) == 'User "testUser" has 0 points'
        assert UserPoint.objects.count() == 1

    def test_direct_reward(self, default_user: User) -> None:
        reward = DirectReward.objects.create(
            name='pizza', user=default_user
        )
        assert str(reward) == '1 - pizza for user "testUser"'
        assert reward.description is None
        assert reward.name == 'pizza'

    def test_point_reward(self, default_user: User) -> None:
        reward = PointReward.objects.create(
            name='The Witcher 3', user=default_user, points=100
        )
        assert str(reward) == '1 - The Witcher 3 (100 pts) for user "testUser"'
        assert reward.description is None
        assert reward.name == 'The Witcher 3'

    def test_goal(self, default_user: User) -> None:
        reward = DirectReward.objects.create(
            name='The Witcher 3', user=default_user
        )
        goal = Goal.objects.create(
            name='Run a marathon', user=default_user, reward_points=30,
            description='Run 40km in Edinburgh this year',
            finish_date=datetime(2020, 12, 31, tzinfo=pytz.UTC),
            direct_reward=reward
        )
        assert str(goal) == '1 - Run a marathon for user "testUser"'
        assert goal.description and goal.direct_reward and goal.name
        assert (goal.finish_date and goal.finish_date.day == 31
                and goal.finish_date.hour == 0)
