from django.urls import path
from tag import views
  
urlpatterns = [
    path('/', views.create_tag),
]