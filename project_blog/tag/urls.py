from django.urls import path

from tag import views


urlpatterns = [
    path('most_used/', views.get_most_used_tag),
]
