from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

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

@receiver(pre_save, sender=Message)
def track_message_edits(sender, instance, **kwargs):
    """
    Signal to track message edits and save old content to MessageHistory
    """
    if instance.pk:  # Only for existing messages (updates)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Content has changed
                # Create history entry with old content
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender,  # Assuming sender is editing
                    edit_reason="Message edited by user"
                )
                # Update message edit tracking fields
                instance.edited = True
                instance.last_edited = timezone.now()
                print(f"Message edit tracked: Message {instance.id} was edited")
        except Message.DoesNotExist:
            pass  # New message, no history to track

@receiver(post_save, sender=Message)
def send_real_time_notification(sender, instance, created, **kwargs):
    """
    Additional signal for potential real-time notifications
    """
    if created:
        print(f"Real-time notification triggered for message: {instance.id}")