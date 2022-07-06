from django.urls import path

from blog import views

urlpatterns = [
    path('create/', views.create_blog),
    path('get/', views.get_blog_detail),
    path('', views.get_blogs_by_tag),
    path('edit/', views.edit_blog),
]
