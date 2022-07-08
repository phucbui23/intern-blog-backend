from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'type', 'subject', 
            'content', 'is_success', 
            'sended_at', 'author', 'is_seen'
        )
        read_only_field = fields
