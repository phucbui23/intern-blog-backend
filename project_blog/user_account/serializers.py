from rest_framework import serializers
from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
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
        except Attachment.DoesNotExist:
            avatar = []
        data['avatar'] = AttachmentSerializer(instance=avatar, many=False).data
        return data


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"
