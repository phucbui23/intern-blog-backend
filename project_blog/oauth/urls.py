from django.urls import path
from oauth import views

urlpatterns = [
    path('log_in', views.log_in),
    path('log_out', views.log_out),
    path('resend', views.resend_email),
    path('forgot_password', views.forgot_password),
    path('reset', views.reset_password),
    path('activate', views.activate),
]
