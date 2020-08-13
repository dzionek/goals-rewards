from typing import Any

from django.db import models
from django.db.models.base import ModelBase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from django.dispatch import receiver


class DirectReward(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='direct_rewards'
    )

    def __str__(self) -> str:
        return f'{self.id} - {self.name} for user "{self.user}"'


class PointReward(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    points = models.IntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='point_rewards'
    )

    def __str__(self) -> str:
        return f'{self.id} - {self.name} ({self.points} pts)' \
               f' for user "{self.user}"'


class Goal(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    reward_points = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
    direct_reward = models.OneToOneField(
        DirectReward, blank=True, null=True, on_delete=models.CASCADE,
        related_name='goal'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='goals'
    )

    def __str__(self) -> str:
        return f'{self.id} - {self.name} for user "{self.user}"'


class UserPoint(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f'User "{self.user.username}" has {self.points} points'


@receiver(post_save, sender=User)
def create_user_point(sender: ModelBase, instance: User,
                      created: bool, **kwargs: Any) -> None:
    if created:
        UserPoint.objects.create(user=instance)
