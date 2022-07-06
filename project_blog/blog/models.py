import uuid

from django.db import models
from user_account.models import User
from attachment.models import Attachment


class Blog(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False, 
        unique=True, 
        max_length=36,
        null=False,
        blank=False,
    )
    name = models.TextField(
        max_length=255,
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='blog_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    # attachment = models.ForeignKey(
    #     to=Attachment,
    #     on_delete=models.CASCADE,
    #     to_field='uid',
    #     related_name='blog_fk_attachment',
    #     db_column='attachment_uid',
    #     db_constraint=False,
    #     null=True,
    #     blank=True,
    # )
    content = models.TextField(
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now=False, 
        auto_now_add=True,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
    )


class BlogHistory(models.Model):
    blog = models.ForeignKey(
        to=Blog, 
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='bloghistory_fk_blog',
        db_column='blog_uid',
        db_constraint=False,
        null=False,
        blank=False,
    )
    revision = models.IntegerField(
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='bloghistory_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    name = models.TextField(
        max_length=255,
        null=False,
        blank=False,
    )
    content = models.TextField(
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        null=False,
        blank=False,
    )
    published_at = models.DateTimeField(
        auto_now=True, 
        auto_now_add=False,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now=False, 
        auto_now_add=True,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (
            ('blog', 'revision',),
        )


class BlogLike(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field='id',
        related_name='bloglike_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    blog = models.ForeignKey(
        to=Blog, 
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='bloglike_fk_blog',
        db_column='blog_uid',
        db_constraint=False,
        null=False,
        blank=False,
    )
    comment = models.TextField(
        null=True, 
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now=False, 
        auto_now_add=True,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    
    class Meta:
        unique_together = (
            ('author', 'blog',),
        )
