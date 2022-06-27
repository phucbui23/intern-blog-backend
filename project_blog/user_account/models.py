from django.db import models
from utils.enums import Gender
from utils.enums import Status
#from blog.models import Blog
#from attachment.models import Attachment
# Create your models here.


class User(models.Model):
    REQUIRED_FIELDS = ['status', 'active', 'created_at', 'is_superuser', 'is_admin']
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
    )
    phone_number = models.CharField(
        max_length=16, 
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
    )
    nick_name = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
    )
    quote = models.TextField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        choices=Gender.choices, 
        default=Gender.OTHER,
    )
    avatar = models.ForeignKey(
        to='attachment.Attachment',
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='user_fk_avatar',
        db_column='avatar_uid',
        db_constraint=False,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices, 
        default=Status.AVAILABLE,
    )
    active = models.BooleanField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        null=True, 
        blank=True,
    )
    is_superuser = models.BooleanField()
    is_admin = models.BooleanField()


class Follower(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='follower_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    follower = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='follower_fk_follower',
        db_column='follower_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    follow_by = models.ForeignKey(
        to='blog.Blog',
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='follower_fk_follower_by',
        db_column='follower_by_uid',
        db_constraint=False,
        null=True,
        blank=True,
    )
    active = models.BooleanField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        null=True, 
        blank=True,
    )
