from django.urls import path

from tag import views


urlpatterns = [
    path('create/', views.create_tag),
]
