from rest_framework import serializers
from user_account.serializers import UserSerializer
from .models import UserActivation, UserDeviceToken, ResetPassword


class UserActivationSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserActivation
        fields = ('author','active','token')
        read_only_fields = fields

class UserDeviceTokenSerialier(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = UserDeviceToken
        fields = ('author','active', 'token',)
        read_only_fields = fields
    

class ResetPasswordSerialier(serializers.ModelSerializer):
    class Meta:
        model = ResetPassword
        fields = ('author','active', 'token')
        read_only_fields = fields
