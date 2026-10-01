from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.SerializerMethodField()

    recipient_email = serializers.CharField(
        source="recipient.email",
        read_only=True
    )

    def get_recipient_name(self, obj):
        first_name = getattr(
            obj.recipient,
            "first_name",
            ""
        )

        last_name = getattr(
            obj.recipient,
            "last_name",
            ""
        )

        full_name = (
            f"{first_name} {last_name}"
        ).strip()

        return (
            full_name
            if full_name
            else obj.recipient.email
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
            "recipient_name",
            "recipient_email",
            "created_at",
        ]