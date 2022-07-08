from django.urls import path
from user_account import views



urlpatterns = [
    path('sign_up', views.sign_up),
    path('edit_profile', views.edit_profile),
    path('info', views.get_user_info),
    path('change_password', views.change_password),
    path('follower/', views.follow_user),
    path('follower/blog', views.follow_by_blog),
]


