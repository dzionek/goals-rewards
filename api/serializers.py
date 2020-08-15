from django.contrib.auth.models import User
from rest_framework import serializers

from system.models import Goal, DirectReward, PointReward


class DirectRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectReward
        fields = ['id', 'name', 'description']


class PointRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointReward
        fields = ['id', 'name', 'description', 'points']


class GoalSerializer(serializers.ModelSerializer):
    direct_reward = DirectRewardSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = [
            'id', 'name', 'description', 'finish_date',
            'reward_points', 'direct_reward'
        ]


class UserSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    direct_rewards = DirectRewardSerializer(many=True, read_only=True)
    point_rewards = PointRewardSerializer(many=True, read_only=True)
    points = serializers.IntegerField(source='userpoint.points')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'points', 'goals',
            'direct_rewards', 'point_rewards'
        ]
