from django.urls import path

from notification import views

urlpatterns = [
    path('', views.get_notifications),
    path('get/', views.access_notification),
    path('seen/', views.seen_notifications),
    path('num_not_seen/', views.num_not_seen_noti),
]
