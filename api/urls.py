from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.GoalList.as_view()),
    path('goals/<int:pk>/', views.GoalDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view())
]
