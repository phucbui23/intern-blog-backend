from django.urls import path
from user_account import views

urlpatterns = [
    path('sign_up', views.sign_up),
    path('edit_profile', views.edit_profile),
    path('change_password', views.change_password),
]
