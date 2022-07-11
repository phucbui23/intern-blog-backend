from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.decorators import api_view
# from rest_framework.decorators import list_route

from utils.api_decorator import json_response
from utils.validate_token import validate_token
from blog.models import Blog, BlogLike

from .models import Notification
from .serializers import NotificationSerializer

        
@receiver(post_save, sender=BlogLike)
def bloglike_created_handler(sender, instance, created, 
                             *args, **kwargs):
    if created:      
        blog_uid = instance.blog.uid  
        
        data = Notification.objects.create(
            type="blog liked",
            subject="Like",
            content=blog_uid,
            author=instance.author,
        )
        
        return data
    else:
        return None
    
@receiver(post_save, sender=Blog)
def blog_created_handler(sender, instance, created, 
                             *args, **kwargs):
    if created:
        data = {}
        data['blog'] = instance.blog
        data['author'] = instance.author
        
        return data
    else:
        return None

# # @list_route()
# def seen_all(request):
#     validate_token(request.auth)
#     user = request.user
    
#     not_seen_notification = Notification.objects.filer(
#         is_seen=False,
#         author=user,
#     )
    
#     not_seen_notification.update(
#         is_seen=True,
#     )
    
#     return NotificationSerializer(
#         not_seen_notification
#     ).data
    
# @receiver(post_save, sender=Blog)
# def create_notification(sender, **kwargs):
#     ...
