from django.urls import path
from user_account import views

urlpatterns = [
    path('create', views.create_user),
    path('followers/create', views.create_follower),
]