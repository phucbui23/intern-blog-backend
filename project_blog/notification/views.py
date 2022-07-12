from django.forms import ValidationError
from rest_framework.decorators import api_view

from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from blog.models import Blog, BlogLike
from blog.serializers import BlogSerializer
from user_account.models import Follower
from utils.api_decorator import json_response
from utils.messages import BLOG_NOT_EXIST

from .models import Notification
from .serializers import NotificationSerializer


@api_view(['POST'])
@json_response
def get_notifications(request):
    user = request.user
    
    notifications = Notification.objects.filter(
        author=user
    ).order_by('-sended_at')
    
    data = NotificationSerializer(
        notifications,
        many=True
    ).data
    
    return data


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
    
    try:
        blog = Blog.objects.get(
            uid=notification.blog.uid
        )
    except Blog.DoesNotExist:
        raise ValidationError(
            message=BLOG_NOT_EXIST
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
    liked = BlogLike.objects.filter(
        author=user,
        blog=blog,
    ).exists()
    
    data['is_liked'] = liked
    
    # check if user have followed the author
    is_followed = Follower.objects.filter(
        author=blog.author,
        follower=user,
        follow_by=blog,
        active=True,
    ).exists()
    
    data['is_followed'] = is_followed
    
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
