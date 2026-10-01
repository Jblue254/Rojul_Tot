# notifications/utils.py

from .models import Notification



def create_notification(
    recipient,
    title,
    message,
    notification_type=Notification.NotificationType.SYSTEM
):
    Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type
    )