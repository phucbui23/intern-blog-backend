from django.urls import path

from notification import views

urlpatterns = [
    path('', views.get_notifications),
    path('get/', views.access_notification),
    path('seen/', views.seen_notifications),
]
