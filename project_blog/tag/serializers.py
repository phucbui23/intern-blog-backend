from rest_framework import serializers

from .models import Tag, BlogTag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name', 'description',
            'created_at', 'updated_at',
        )
        read_only_fields = fields
        
class BlogTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=False)
    class Meta:
        model = BlogTag
        fields = ('tag',)
        read_only_fields = ('blog', 'tag',)
