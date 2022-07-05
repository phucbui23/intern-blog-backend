from dataclasses import field
from rest_framework import serializers
from .models import Attachment

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = (
            'uid', 'user', 'type',
            'file_name', 'display_name', 'file_path',
            'is_deleted', 'created_at',
        )
        read_only_fields = fields
    