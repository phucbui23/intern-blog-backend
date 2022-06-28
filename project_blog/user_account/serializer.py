from rest_framework import serializers
from user_account.models import User, Follower

class UserSerialier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"