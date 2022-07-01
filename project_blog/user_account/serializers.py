from rest_framework import serializers
from user_account.models import User, Follower


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number',
                  'full_name', 'nick_name', 'quote',)
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        follower = Follower.objects.filter(
            author=instance
        )
        data['follower'] = FollowerSerializer(follower, many=True).data

        return data


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"
