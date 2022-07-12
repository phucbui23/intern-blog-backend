from django.db import models

from blog.models import Blog
from user_account.models import User
from utils.enums import Notification_type


class Notification(models.Model):
    type = models.TextField(
        choices=Notification_type.choices, 
        default=Notification_type.BLOG_LIKED,
    )
    
    subject = models.TextField(
        null=False,
        blank=False,
    )
    
    content = models.TextField(
        null=False,
        blank=False,
    )
    
    is_success = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    
    sended_at = models.DateTimeField(
        auto_now=True, 
        auto_now_add=False,
        null=True, 
        blank=True,
    )
    
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='notification_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    
    blog = models.ForeignKey(
        to=Blog, 
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='notification_fk_blog',
        db_column='blog_uid',
        db_constraint=False,
        null=False,
        blank=False,
    )
    
    is_seen = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
