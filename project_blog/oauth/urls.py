from django.urls import path
from oauth import views

urlpatterns = [
    path('log_in', views.log_in),
    path('resend', views.resend_email),
    path('forgot_password', views.forgot_password),
    path('reset/<str:token>', views.reset_password),
    path('activate/<str:token>', views.activate),
]