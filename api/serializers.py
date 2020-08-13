from django.contrib.auth.models import User
from rest_framework import serializers

from system.models import Goal, DirectReward, PointReward


class DirectRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectReward
        fields = ['name', 'description']


class PointRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointReward
        fields = ['name', 'description', 'points']


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

    class Meta:
        model = User
        fields = ['id', 'username', 'goals', 'direct_rewards']
