from rest_framework import serializers

from user_account.models import User
from user_account.serializers import UserSerializer

from .models import UserActivation, UserDeviceToken, ResetPassword


class UserActivationSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserActivation
        fields = ('author','active','token')
        read_only_fields = fields
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        author = User.objects.get(
            email=instance,
        )
        data['author'] = UserSerializer(author, many=False).data
        return data

class UserDeviceTokenSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserDeviceToken
        fields = ('author','active', 'token',)
        read_only_fields = fields
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        author = User.objects.get(
            email=instance,
        )
        data['author'] = UserSerializer(instance=author, many=False).data
        return data

class ResetPasswordSerialier(serializers.ModelSerializer):
    class Meta:
        model = ResetPassword
        fields = ('author','active', 'token')
        read_only_fields = fields
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        author = User.objects.get(
            email=instance,
        )
        data['author'] = UserSerializer(author, many=False).data
        return data


