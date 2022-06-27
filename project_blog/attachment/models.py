import uuid

from django.db import models
from user_account.models import User
from utils.enums import Attachment_type

# Create your models here.


class Attachment(models.Model):
    uid = models.CharField(
        default=uuid.uuid4(),
        primary_key=True,
        editable=False, 
        unique=True, 
        max_length=36,
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
        default=Attachment_type.AVA,
    )

    file_name = models.CharField(
        max_length=225,
    )

    display_name = models.CharField(
        max_length=225,
    )

    file_path = models.TextField()

    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
    )

    delete = models.BooleanField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True, 
        null=True, 
        blank=True,
    )
