from django.urls import path
from user_account import views

urlpatterns = [
    path('sign_up', views.sign_up),
    path('log_in', views.log_in),
    path('edit_profile', views.edit_profile),
    path('change_password', views.change_password),
    path('activate/<str:token>', views.activate),
    path('reset', views.reset_password),
    path('reset/<str:token>', views.confirm_reset_password),
]