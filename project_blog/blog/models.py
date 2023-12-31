import uuid

from attachment.models import Attachment
from django.db import models
from django.forms import ValidationError
from user_account.models import Follower, User
from utils.messages import (BLOG_NOT_EXIST, MAX_LENGTH_BLOG_CONTENT,
                            MAX_LENGTH_BLOG_NAME)


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
    
    @staticmethod
    def get_total_blog_by_user(author:User, *args, **kwargs):
        try:
            return Blog.objects.filter(
                author=author,
                is_published=True,
            ).count()
        except Blog.DoesNotExist:
            raise ValidationError(BLOG_NOT_EXIST)

    def is_valid(self):
        if (len(self.name) > 255):
            raise ValidationError(MAX_LENGTH_BLOG_NAME)
        if (len(self.content) > 255):
            raise ValidationError(MAX_LENGTH_BLOG_CONTENT)
    
    def save(self, *args, **kwargs):
        if (self.pk):
            blog_history = BlogHistory.objects.filter(
                blog=self
            ).aggregate(models.Max('revision'))
        
            new_blog_history = BlogHistory.objects.create(
                revision=blog_history['revision__max']+1 if (blog_history['revision__max']) else 1,
                name=self.name,
                content=self.content,
                is_published=self.is_published,
                blog=self,
                author=self.author,
            )
        return super().save(*args, **kwargs)
   
    @staticmethod
    def get_latest_blog(author:User):
        return Blog.objects.filter(author=author).order_by('-created_at').first()

    # def __str__(self) -> str:
    #     return f"{self.name} - {self.author.email}"

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
    
    @staticmethod
    def get_most_liked_blog(author:User):
        return Blog.objects.filter(
            author=author
        ).prefetch_related(
            'bloglike_fk_blog'
        ).annotate(
            like=models.Count('bloglike_fk_blog')
        ).order_by(
            '-like'
        ).first()

    class Meta:
        unique_together = (
            ('author', 'blog',),
        )
