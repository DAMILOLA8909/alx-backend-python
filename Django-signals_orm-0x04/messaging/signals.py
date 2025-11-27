from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to automatically create a notification when a new message is created
    """
    if created:
        # Create notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type='message'
        )
        print(f"Notification created for {instance.receiver.username}")

@receiver(post_save, sender=Message)
def send_real_time_notification(sender, instance, created, **kwargs):
    """
    Additional signal for potential real-time notifications
    (WebSocket, email, push notifications can be added here)
    """
    if created:
        # Placeholder for real-time notification logic
        # This could integrate with WebSockets, email services, etc.
        print(f"Real-time notification triggered for message: {instance.id}")