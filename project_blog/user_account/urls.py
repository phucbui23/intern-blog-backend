from django.urls import path
from user_account import views

urlpatterns = [
    path('/', views.create_user),
    path('/followers', views.create_follower),
]