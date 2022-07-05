from django.urls import path
from tag import views
  
urlpatterns = [
    path('create/', views.create_tag),
    path('get/', views.get_tag),
    path('', views.get_tag_by_blog),
    path('blogtag/', views.create_blogtag),
    path('edit/', views.edit_tag),
]