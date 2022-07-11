from attachment.serializers import AttachmentSerializer
from rest_framework import serializers

from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from tag.serializers import TagSerializer
from tag.models import Tag
from user_account.models import User

from .models import (
    Blog, 
    BlogAttachment, 
    BlogHistory, 
    BlogLike
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number',
                  'full_name', 'nick_name', 'quote','avatar')
        read_only_fields = fields


class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    attachment = AttachmentSerializer(read_only=True, many=False)
    author = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Blog
        fields = (
            'uid', 'name', 'author', 'tags', 'attachment' ,'content',
            'is_published', 'created_at',
        )
        read_only_field = fields
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        try:
            blog_attachment = BlogAttachment.objects.filter(
                blog=instance
            ).first()
            
            if blog_attachment != None:
                thumbnail = blog_attachment.attachment
                data['thumbnail'] = AttachmentSerializer(
                    instance=thumbnail, 
                    many=False
                ).data
            else:
                data['thumbnail'] = None
        except Attachment.DoesNotExist:
            thumbnail = None
            
        try:
            tags = Tag.objects.prefetch_related(
                'blogtag_fk_tag'
            ).filter(
                blogtag_fk_tag__blog=instance
            )
            
            data['tags'] = TagSerializer(
                instance=tags,
                many=True
            ).data
        except Tag.DoesNotExist:
            tags = None  
            
        try:
            likes = BlogLike.objects.filter(
                blog=instance
            ).count()
            
            data['likes'] = likes
        except BlogLike.DoesNotExist:
            likes = 0
            
        return data
        
class BlogAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogAttachment
        fields = ('blog', 'attachment', 'created_at',
                  'updated_at',)
        read_only_fields = ('blog', 'attachment',)
            
class BlogHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogHistory
        fields = (
            'blog', 'revision', 'author',
            'name', 'is_published', 'created_at',
        )
        read_only_field = fields

class BlogLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogLike
        fields = [
            'author', 'blog', 'comment',
            'created_at', 'updated_at',
        ]
        read_only_field = fields
