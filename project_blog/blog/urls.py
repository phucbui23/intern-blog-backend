from django.urls import path

from blog import views

urlpatterns = [
    path('create/', views.create_blog),
    path('get/', views.get_matrix_blogs),
    path('bytag/', views.get_blogs_by_tag),
    path('edit/', views.edit_blog),
    path('detail/', views.get_blog_detail),
    path('like/', views.create_blog_like),
    path('unlike/', views.blog_unlike),
    path('delete/', views.delete_blog),
    path('my_blog/', views.get_user_blog),
    path('new_blogs/', views.get_new_blog),
    path('get_likes/', views.get_blog_likes),
]
