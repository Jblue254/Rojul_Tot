from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(
        source="recipient.full_name",
        read_only=True
    )

    recipient_email = serializers.CharField(
        source="recipient.email",
        read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "recipient_name",
            "recipient_email",
            "title",
            "message",
            "notification_type",
            "is_read",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]