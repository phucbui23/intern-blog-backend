from django.db import models

from user_account.models import User


class Notification(models.Model):
    type = models.TextField(
        null=False,
        blank=False,
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
    
    is_seen = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
