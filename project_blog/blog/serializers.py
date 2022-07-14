from rest_framework import serializers

from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from tag.serializers import BlogTagSerializer
from tag.models import Tag
from user_account.models import User, Follower

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

class BlogAttachmentSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(read_only=True)
    class Meta:
        model = BlogAttachment
        fields = ('attachment',)
        read_only_fields = ('blog', 'attachment',)

class BlogSerializer(serializers.ModelSerializer):
    tags = BlogTagSerializer(read_only=True, many=True)
    attachment = BlogAttachmentSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True, many=False)
    likes = serializers.IntegerField(read_only=True, source='num_of_likes')

    class Meta:
        model = Blog
        fields = (
            'uid', 'name', 'author', 'tags', 'attachment' ,'content',
            'is_published', 'created_at', 'likes',
        )
        read_only_field = fields
        
            
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
