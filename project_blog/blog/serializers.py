from rest_framework import serializers

from .models import Blog, BlogHistory, BlogLike


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'uid',
            'name',
            'author',
            'content',
            'is_published',
            'published_at',
            'created_at',
            'updated_at',
        ]

class BlogHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogHistory
        fields = [
            'blog',
            'revision',
            'author',
            'name',
            'content',
            'is_published',
            'published_at',
            'created_at',
            'updated_at',
        ]

class BlogLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogLike
        fields = [
            'author',
            'blog',
            'comment',
            'created_at',
            'updated_at',
        ]

