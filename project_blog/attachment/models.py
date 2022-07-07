import uuid

from django.db import models
from user_account.models import User
from utils.enums import Attachment_type

# Create your models here.


class Attachment(models.Model):
    uid = models.CharField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False, 
        unique=True, 
        max_length=36,
        null=False,
        blank=False
    )

    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='attachment_fk_user',
        db_column='user_id',
        db_constraint=False,
        null=False,
        blank=False,
    )

    type = models.CharField(
        max_length=32, 
        choices=Attachment_type.choices, 
        default=Attachment_type.AVATAR,
        null=False,
        blank=False,
    )

    file_name = models.CharField(
        max_length=225,
        null=False,
        blank=False,
    )

    display_name = models.CharField(
        max_length=225,
        null=False,
        blank=False,
    )

    file_path = models.TextField(
        null=False,
        blank=False,
    )

    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
    )

    is_deleted = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True, 
        null=True, 
        blank=True,
    )
    
    @staticmethod
    def get_attachment(uid):
        attachment = Attachment.objects.get(uid=uid)
        return attachment
