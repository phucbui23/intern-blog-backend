from django.db import models
from user_account.models import User
# Create your models here.
class Notification(models.Model):
    type = models.TextField()
    subject = models.TextField()
    content = models.TextField()
    is_success = models.BooleanField()
    sended_at = models.DateTimeField(
        auto_now=True, 
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
    is_seen = models.BooleanField()