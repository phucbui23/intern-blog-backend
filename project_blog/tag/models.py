from django.db import models
from user_account.models import User
from blog.models import Blog

class Tag(models.Model):
    name = models.TextField(
        max_length=255,
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='tag_fk_author',
        db_column='author_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    description = models.TextField(
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
    
class BlogTag(models.Model):
    blog = models.ForeignKey(
        to=Blog, 
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='blogtag_fk_blog',
        db_column='blog_id',
        db_constraint=False,
        null=False,
        blank=False,
    )
    tag = models.ForeignKey(
        to=Tag, 
        on_delete=models.CASCADE,
        to_field='id',
        related_name='blogtag_fk_tag',
        db_column='tag_id',
        db_constraint=False,
        null=False,
        blank=False,
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
            ('blog', 'tag',),
        )