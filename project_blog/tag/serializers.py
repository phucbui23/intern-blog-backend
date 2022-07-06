from rest_framework import serializers

from .models import Tag, BlogTag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'author', 'description',
                  'created_at', 'updated_at',)
        read_only_fields = fields
        
class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ('blog', 'tag', 'created_at',
                  'updated_at',)
        read_only_fields = ('blog', 'tag',)
