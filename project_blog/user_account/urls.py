from django.urls import path
from user_account import views

urlpatterns = [
    path('/', views.get_list_user),
    path('/create-user', views.create_user),
    path('/followers', views.create_follower),
]