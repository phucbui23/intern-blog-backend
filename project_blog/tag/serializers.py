from rest_framework import serializers
from .models import Tag, BlogTag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        
class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"