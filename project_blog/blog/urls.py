from django.urls import path
from blog import views

urlpatterns = [
    path('create/', views.create_blog),
    path('get/<str:uid>/', views.get_blog_detail),
    path('edit/', views.edit_blog),
]