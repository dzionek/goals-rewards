from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='system_home'),
    path('add-point-reward', views.add_point_reward,
         name='system_add_point_reward'),
    path('add-direct-reward', views.add_direct_reward,
         name='system_add_direct_reward'),
    path('add-goal', views.add_goal, name='system_add_goal')
]
