from django.urls import path
from blog import views

urlpatterns = [
    path('create/', views.create_blog),
    path('get/', views.get_blog),
    path('edit/', views.edit_blog),
]