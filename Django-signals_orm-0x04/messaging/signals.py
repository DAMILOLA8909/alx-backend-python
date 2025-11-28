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
        # Determine notification type based on whether it's a reply
        notification_type = 'reply' if instance.parent_message else 'message'
        
        # Create notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type=notification_type
        )
        print(f"Notification created for {instance.receiver.username} (Type: {notification_type})")

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
                    edited_by=instance.sender,
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
    """
    user_id = instance.id
    username = instance.username
    
    print(f"Cleaning up data for deleted user: {username} (ID: {user_id})")
    
    # Delete notifications for this user using ID
    user_notifications = Notification.objects.filter(user_id=user_id)
    notifications_count = user_notifications.count()
    user_notifications.delete()
    print(f"Deleted {notifications_count} user notifications")
    
    # Delete message history entries where user was the editor using ID
    edit_history = MessageHistory.objects.filter(edited_by_id=user_id)
    history_count = edit_history.count()
    edit_history.delete()
    print(f"Deleted {history_count} message edit history entries")
    
    # Additional cleanup for any orphaned data
    orphaned_notifications = Notification.objects.filter(message__isnull=True)
    orphaned_notifications_count = orphaned_notifications.count()
    if orphaned_notifications_count > 0:
        orphaned_notifications.delete()
        print(f"Cleaned up {orphaned_notifications_count} orphaned notifications")
    
    orphaned_history = MessageHistory.objects.filter(message__isnull=True)
    orphaned_history_count = orphaned_history.count()
    if orphaned_history_count > 0:
        orphaned_history.delete()
        print(f"Cleaned up {orphaned_history_count} orphaned message history entries")
    
    print(f"Cleanup completed for user: {username}")

@receiver(post_save, sender=Message)
def send_real_time_notification(sender, instance, created, **kwargs):
    """
    Additional signal for potential real-time notifications
    """
    if created:
        message_type = "reply" if instance.parent_message else "message"
        print(f"Real-time notification triggered for {message_type}: {instance.id}")