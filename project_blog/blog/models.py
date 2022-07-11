import uuid
from django.db import models

from user_account.models import User
from attachment.models import Attachment
from django.forms import ValidationError
from utils.messages import BLOG_NOT_EXIST, MAX_LENGTH_BLOG_NAME, MAX_LENGTH_BLOG_CONTENT

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
    
    @staticmethod
    def get_by_uid(uid:str):
        try:
            return Blog.objects.get(uid=uid)
        except Blog.DoesNotExist:
            raise ValidationError(BLOG_NOT_EXIST)
        
    def is_valid(self):
        if (len(self.name) > 255):
            raise ValidationError(MAX_LENGTH_BLOG_NAME)
        if (len(self.content) > 255):
            raise ValidationError(MAX_LENGTH_BLOG_CONTENT)
    
    def save(self, *args, **kwargs):
        if not (self.pk):
            revision = BlogHistory.objects.filter(
                blog=self
            ).aggregate(models.Max('revision'))
        
            BlogHistory.objects.create(
                revision=revision+1 if (revision) else 1,
                name=self.name,
                content=self.content,
                is_published=self.is_published,
                blog=self,
                author=self.author,
            )
        return super().save(*args, **kwargs)
   
        
class BlogAttachment(models.Model):
    blog = models.ForeignKey(
        to=Blog, 
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='blogattachment_fk_blog',
        db_column='blog_uid',
        db_constraint=False,
        null=False,
        blank=False,
    )
    attachment = models.ForeignKey(
        to=Attachment, 
        on_delete=models.CASCADE,
        to_field='uid',
        related_name='blogattachment_fk_attachment',
        db_column='attachment_uid',
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
    
    @staticmethod
    def get_attachments_in_blog(blog):
        try:
            blogattachment = BlogAttachment.objects.filter(
                blog=blog
            )
        except BlogAttachment.DoesNotExist:
            blogattachment = None
        return blogattachment

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
