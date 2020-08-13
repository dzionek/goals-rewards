from django.contrib.auth.models import User
from rest_framework import generics

from system.models import Goal
from .serializers import (UserSerializer, GoalSerializer)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GoalList(generics.ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class GoalDetail(generics.RetrieveAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
