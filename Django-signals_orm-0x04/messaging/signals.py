from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
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

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all related data when a user is deleted
    This handles data that isn't covered by CASCADE deletion
    """
    print(f"Cleaning up data for deleted user: {instance.username}")
    
    # Delete messages where user is sender or receiver
    # These should be handled by CASCADE, but we'll log them
    sent_messages = Message.objects.filter(sender=instance)
    received_messages = Message.objects.filter(receiver=instance)
    
    print(f"Deleting {sent_messages.count()} sent messages")
    print(f"Deleting {received_messages.count()} received messages")
    
    # Delete notifications for this user
    user_notifications = Notification.objects.filter(user=instance)
    print(f"Deleting {user_notifications.count()} user notifications")
    user_notifications.delete()
    
    # Delete message history entries where user was the editor
    edit_history = MessageHistory.objects.filter(edited_by=instance)
    print(f"Deleting {edit_history.count()} message edit history entries")
    edit_history.delete()
    
    # Additional cleanup for any orphaned data
    # Notifications for messages that no longer exist (should be handled by CASCADE)
    orphaned_notifications = Notification.objects.filter(message__isnull=True)
    if orphaned_notifications.exists():
        print(f"Cleaning up {orphaned_notifications.count()} orphaned notifications")
        orphaned_notifications.delete()
    
    # Message history for messages that no longer exist
    orphaned_history = MessageHistory.objects.filter(message__isnull=True)
    if orphaned_history.exists():
        print(f"Cleaning up {orphaned_history.count()} orphaned message history entries")
        orphaned_history.delete()
    
    print(f"Cleanup completed for user: {instance.username}")

@receiver(post_save, sender=Message)
def send_real_time_notification(sender, instance, created, **kwargs):
    """
    Additional signal for potential real-time notifications
    """
    if created:
        print(f"Real-time notification triggered for message: {instance.id}")