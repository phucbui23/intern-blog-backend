from rest_framework import serializers
from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from blog.models import Blog
from blog.serializers import BlogSerializer
from .models import User, Follower



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number',
                  'full_name', 'nick_name', 'quote','avatar')
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        try:    
            avatar = Attachment.objects.get(
                user=instance,
            )
            avatar_data = AttachmentSerializer(instance=avatar, many=False).data
            avatar_data.pop('user')
            data['avatar'] = avatar_data
        except Attachment.DoesNotExist:
            avatar = None
            
        return data


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('author', 'follower', 'follow_by','active')
        read_only_fields = fields
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        author = User.objects.get(pk=instance.author_id)
        follower = User.objects.get(pk=instance.follower_id)

        if instance.follow_by_id:
            follow_by = Blog.objects.get(pk=instance.follow_by_id)
            data['follow_by'] = BlogSerializer(instance=follow_by, many=False).data

        data['author'] = UserSerializer(instance=author, many=False).data
        data['follower'] = UserSerializer(instance=follower, many=False).data
        
        return data
        