from typing import Type

from django.contrib.auth.models import User
from django.db.models import Model, QuerySet

from rest_framework.serializers import ModelSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from system.models import Goal, DirectReward, PointReward
from .serializers import (UserSerializer, GoalSerializer,
                          DirectRewardSerializer, PointRewardSerializer)


# Admin-restricted views
def admin_api_view_set_factory(serializer: Type[ModelSerializer],
                               model: Type[Model]) -> Type[GenericViewSet]:

    class AdminViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       GenericViewSet):

        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = [IsAdminUser]

    return AdminViewSet


AdminUserViewSet = admin_api_view_set_factory(
    UserSerializer, User
)

AdminGoalViewSet = admin_api_view_set_factory(
    GoalSerializer, Goal
)

AdminDirectRewardViewSet = admin_api_view_set_factory(
    DirectRewardSerializer, DirectReward
)

AdminPointRewardViewSet = admin_api_view_set_factory(
    PointRewardSerializer, PointReward
)


# User-specific views
def user_api_view_set_factory(serializer: Type[ModelSerializer],
                              model: Type[Model]) -> Type[GenericViewSet]:

    class ViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  GenericViewSet):
        serializer_class = serializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self) -> QuerySet:
            user = self.request.user
            return model.objects.filter(user=user).all()

    return ViewSet


GoalViewSet = user_api_view_set_factory(
    GoalSerializer, Goal
)

DirectRewardViewSet = user_api_view_set_factory(
    DirectRewardSerializer, DirectReward
)

PointRewardViewSet = user_api_view_set_factory(
    PointRewardSerializer, PointReward
)
