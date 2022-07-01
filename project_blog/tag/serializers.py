from rest_framework import serializers
from .models import Tag, BlogTag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'author', 'description',)
        read_only_fields = fields