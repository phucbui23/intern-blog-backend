from rest_framework import serializers
from attachment.models import Attachment
from attachment.serializers import AttachmentSerializer
from .models import User, Follower



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number',
                  'full_name', 'nick_name', 'quote',)
        read_only_fields = fields

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     avatar = Attachment.objects.get(
    #         user=instance,
    #     )
    #     data['avatar'] = AttachmentSerializer(instance=avatar, many=False).data
    #     return data


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"
