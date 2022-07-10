from rest_framework import serializers
from email_logs.models import EmailLogs


class EmailLogsSerialier(serializers.ModelSerializer):
    class Meta:
        model = EmailLogs
        fields = ('author','type', 'subject')
        read_only_fields = fields
        