from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from blog.serializers import BlogSerializer
from rest_framework import serializers

from .models import Follower, User


class UserSerializer(serializers.ModelSerializer):
    avatar = AttachmentSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number',
                  'full_name', 'nick_name', 'quote','avatar')
        read_only_fields = fields


class FollowerSerializer(serializers.ModelSerializer):

    total_blog = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True)
    follow_by = BlogSerializer(read_only=True)
    most_liked_blog = BlogSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ('author', 'follow_by','active', 'total_blog', 'most_liked_blog',)
        read_only_fields = fields
