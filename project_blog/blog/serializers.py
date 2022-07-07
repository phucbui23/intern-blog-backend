from rest_framework import serializers

from .models import (
    Blog, 
    BlogAttachment, 
    BlogHistory, 
    BlogLike
)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'uid', 'name', 'author', 'content',
            'is_published', 'created_at',
        )
        read_only_field = fields
        
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
