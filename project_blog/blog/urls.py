from django.urls import path

from blog import views

urlpatterns = [
    path('create/', views.create_blog),
    path('get/', views.get_blogs),
    path('get/?page=<int:page>/', views.get_blogs),
    path('bytag/', views.get_blogs_by_tag),
    path('edit/', views.edit_blog),
    path('', views.get_blog_detail),
    path('like/', views.create_blog_like),
    path('unlike/', views.blog_unlike),
    path('delete/', views.delete_blog),
]
