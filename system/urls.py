from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='system_home'),
]
