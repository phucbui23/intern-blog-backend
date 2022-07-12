from rest_framework.decorators import api_view

from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from blog.models import Blog, BlogLike
from blog.serializers import BlogSerializer
from utils.api_decorator import json_response

from .models import Notification
from .serializers import NotificationSerializer


@api_view(['POST'])
@json_response
def get_notifications(request):
    user = request.user
    
    notificaions = Notification.objects.filter(
        author=user
    )
    
    return NotificationSerializer(
        instance=notificaions,
        many=True
    ).data


@api_view(['POST'])
@json_response
def access_notification(request):
    user = request.user
    notification_id = request.query_params.get('id')
    
    notification = Notification.objects.get(
        author=user,
        id=notification_id
    )
    
    notification.is_seen = True
    notification.save()
    
    blog = Blog.objects.get(
        uid=notification.blog.uid
    )
    
    data = BlogSerializer(
        instance=blog
    ).data
    
    # get attachments in a blog
    attachments = Attachment.objects.prefetch_related(
        'blogattachment_fk_attachment'
    ).filter(
        blogattachment_fk_attachment__blog=blog
    )
    
    data['attachments'] = AttachmentSerializer(
        instance=attachments,
        many=True
    ).data
    
    # check if user have liked the blog
    liked = BlogLike.objects.get(
        author=user,
        blog=blog,
    )
    
    data['liked'] = True if (liked) else False
    
    return data
    
    
@api_view(['POST'])
@json_response
def seen_notifications(request):
    user = request.user
    
    not_seen_notifications = Notification.objects.filter(
        author=user,
        is_seen=False
    )
    
    for notification in not_seen_notifications:
        notification.is_seen=True
        notification.save()
        
    notificaions = Notification.objects.filter(
        author=user
    )
    
    return NotificationSerializer(
        instance=notificaions,
        many=True,
    ).data
