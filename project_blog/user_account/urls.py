from django.urls import path
from user_account import views

urlpatterns = [
    path('sign_up', views.sign_up),
    path('log_in', views.log_in),
    #path('logout', views.log_out),
    path('activate/<str:token>', views.activate),
]