from django.urls import path
from blog import views

urlpatterns = [
    path('create', views.create_blog),

]