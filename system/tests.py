import pytest
from datetime import date

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from tests.helpers import check_login_required
from .models import DirectReward, PointReward, UserPoint, Goal


@pytest.mark.django_db
class TestRoutes:
    def test_home(self, client: Client, default_user: User) -> None:
        check_login_required(client, 'system_home')
        client.force_login(default_user)

        response = client.get(reverse('system_home'))
        assert response.status_code == 200
        assert 'Welcome in ' in response.content.decode()

    def test_add_point_reward(self, client: Client,
                              default_user: User) -> None:

        check_login_required(client, 'system_add_point_reward')
        client.force_login(default_user)

        response = client.get(reverse('system_add_point_reward'), follow=True)
        assert response.status_code == 200
        assert 'Add Point Reward' in response.content.decode()

        response = client.post(
            reverse('system_add_point_reward'),
            dict(name='Pizza', points=50), follow=True
        )
        assert response.status_code == 200

        assert PointReward.objects.count() == 1
        point_reward = PointReward.objects.first()
        assert point_reward and point_reward.user == default_user
        assert not point_reward.description
        assert point_reward.name == 'Pizza'

    def test_add_direct_reward(self, client: Client,
                               default_user: User) -> None:

        check_login_required(client, 'system_add_direct_reward')
        client.force_login(default_user)

        response = client.get(reverse('system_add_direct_reward'), follow=True)
        assert response.status_code == 200
        assert 'Add Direct Reward' in response.content.decode()

        response = client.post(
            reverse('system_add_direct_reward'),
            dict(name='Pizza', description='All pizza for me!'), follow=True
        )
        assert response.status_code == 200

        assert DirectReward.objects.count() == 1
        direct_reward = DirectReward.objects.first()
        assert direct_reward and direct_reward.user == default_user
        assert direct_reward.description == 'All pizza for me!'
        assert direct_reward.name == 'Pizza'

    def test_add_goal(self, client: Client, default_user: User) -> None:
        check_login_required(client, 'system_add_goal')
        client.force_login(default_user)

        response = client.get(reverse('system_add_goal'), follow=True)
        assert response.status_code == 200
        assert 'Add Goal' in response.content.decode()

        DirectReward.objects.create(name='New keyboard', user=default_user)
        response = client.post(
            reverse('system_add_goal'),
            dict(name='Go to the gym 3 times', reward_points=40,
                 direct_reward=1, finish_date=date(2020, 12, 31)),
            follow=True
        )
        assert response.status_code == 200
        assert 'The goal was successfully added!' in response.content.decode()
        assert Goal.objects.count() == 1

        goal = Goal.objects.first()
        assert goal
        assert isinstance(goal.direct_reward, DirectReward)
        assert goal.direct_reward.name == 'New keyboard'
        assert not goal.description


@pytest.mark.django_db
class TestModels:
    def test_user_point(self, default_user: User) -> None:
        user_point = UserPoint.objects.first()
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
            finish_date=date(2020, 12, 31),
            direct_reward=reward
        )
        assert str(goal) == '1 - Run a marathon for user "testUser"'
        assert goal.description and goal.direct_reward and goal.name
        assert goal.finish_date and goal.finish_date.day == 31
