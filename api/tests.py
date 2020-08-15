import pytest
import json

from django.contrib.auth.models import User
from django.test import Client

from system.models import Goal, DirectReward, PointReward

from tests.helpers import (check_view_set_admin_restricted,
                           check_view_set_user_restricted)


@pytest.mark.django_db
class TestRoutes:
    def test_admin_user_view_set(self, client: Client, default_user: User,
                                 admin_user: User) -> None:
        tested_url = '/api/admin/users/'
        response = check_view_set_admin_restricted(
            client, tested_url, default_user, admin_user
        )

        json_response = json.loads(response.content)
        assert len(json_response) == 2
        assert json_response[0]['username'] == 'testUser'
        assert json_response[1]['point_rewards'] == []

        # Detail
        response = client.get(f'{tested_url}1/')
        json_response = json.loads(response.content)
        assert json_response['username'] == 'testUser'

    def test_admin_goal_view_set(self, client: Client, default_user: User,
                                 admin_user: User) -> None:
        tested_url = '/api/admin/goals/'
        response = check_view_set_admin_restricted(
            client, tested_url, default_user, admin_user
        )

        json_response = json.loads(response.content)
        assert len(json_response) == 0
        Goal.objects.create(
            name='testGoal', user=default_user, reward_points=10
        )

        response = client.get(tested_url)
        assert response.status_code == 200

        json_response = json.loads(response.content)
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'testGoal'
        assert json_response[0]['reward_points'] == 10
        assert json_response[0]['description'] is None

        # Detail
        response = client.get(f'{tested_url}1/')
        json_response = json.loads(response.content)
        assert json_response['name'] == 'testGoal'
        assert json_response['reward_points'] == 10
        assert json_response['finish_date'] is None

    def test_admin_direct_reward_view_set(self, client: Client,
                                          default_user: User,
                                          admin_user: User) -> None:
        tested_url = '/api/admin/direct-rewards/'
        response = check_view_set_admin_restricted(
            client, tested_url, default_user, admin_user
        )

        json_response = json.loads(response.content)
        assert len(json_response) == 0
        DirectReward.objects.create(name='testDirectReward', user=default_user)

        response = client.get(tested_url)
        assert response.status_code == 200

        json_response = json.loads(response.content)
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'testDirectReward'
        assert json_response[0]['description'] is None

        # Detail
        response = client.get(f'{tested_url}1/')
        json_response = json.loads(response.content)
        assert json_response['name'] == 'testDirectReward'

    def test_admin_point_reward_view_set(self, client: Client,
                                         default_user: User,
                                         admin_user: User) -> None:
        tested_url = '/api/admin/point-rewards/'
        response = check_view_set_admin_restricted(
            client, tested_url, default_user, admin_user
        )

        json_response = json.loads(response.content)
        assert len(json_response) == 0
        PointReward.objects.create(
            name='testPointReward', points=20, user=default_user
        )

        response = client.get(tested_url)
        assert response.status_code == 200

        json_response = json.loads(response.content)
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'testPointReward'
        assert json_response[0]['description'] is None
        assert json_response[0]['points'] == 20

        # Detail
        response = client.get(f'{tested_url}1/')
        json_response = json.loads(response.content)
        assert json_response['name'] == 'testPointReward'
        assert json_response['points'] == 20

    def test_user_goal_view_set(self, client: Client, admin_user: User,
                                default_user: User) -> None:
        tested_url = '/api/goals/'
        response = check_view_set_user_restricted(
            client, tested_url, default_user
        )
        json_response = json.loads(response.content)
        assert len(json_response) == 0

        Goal.objects.create(
            name='testGoal', user=default_user, reward_points=10
        )
        Goal.objects.create(
            name='other', user=admin_user, reward_points=33
        )

        response = client.get(tested_url)
        json_response = json.loads(response.content)
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'testGoal'

        # Detail
        response = client.get(f'{tested_url}1/')
        json_response = json.loads(response.content)
        assert json_response['reward_points'] == 10

        response = client.get(f'{tested_url}2/')
        assert response.status_code == 404

    def test_user_direct_reward_view_set(self, client: Client,
                                         admin_user: User,
                                         default_user: User) -> None:
        tested_url = '/api/direct-rewards/'
        response = check_view_set_user_restricted(
            client, tested_url, default_user
        )
        json_response = json.loads(response.content)
        assert len(json_response) == 0

        DirectReward.objects.create(
            name='testDirectReward', user=default_user
        )
        DirectReward.objects.create(
            name='other', description='other', user=admin_user
        )

        response = client.get(tested_url)
        json_response = json.loads(response.content)
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'testDirectReward'

        # Detail
        response = client.get(f'{tested_url}1/')
        json_response = json.loads(response.content)
        assert json_response['description'] is None

    def test_user_point_reward_view_set(self, client: Client,
                                        admin_user: User,
                                        default_user: User) -> None:
        tested_url = '/api/point-rewards/'
        response = check_view_set_user_restricted(
            client, tested_url, default_user
        )
        json_response = json.loads(response.content)
        assert len(json_response) == 0

        PointReward.objects.create(
            name='testPointReward', user=default_user, points=10
        )
        PointReward.objects.create(
            name='other', description='other', user=admin_user, points=33
        )

        response = client.get(tested_url)
        json_response = json.loads(response.content)
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'testPointReward'
        assert json_response[0]['points'] == 10

        # Detail
        response = client.get(f'{tested_url}1/')
        json_response = json.loads(response.content)
        assert json_response['description'] is None
        assert json_response['points'] == 10
