from django.urls import path
from user_account import views

urlpatterns = [
    path('sign-up', views.create_user),
    path('login', views.login),
    path('logout', views.log_out),
    path('activate/<str:uid>/<str:token>', views.activate),
    path('followers', views.create_follower),
]