from rest_framework import serializers
from oauth.models import UserActivation, UserDeviceToken, ResetPassword


class UserActivationSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserActivation
        fields = ('author','active',)
        read_only_fields = fields

class UserDeviceTokenSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserDeviceToken
        fields = ('author','active', 'token',)
        read_only_fields = fields

class ResetPasswordSerialier(serializers.ModelSerializer):
    class Meta:
        model = ResetPassword
        fields = ('author','active', )
        read_only_fields = fields


