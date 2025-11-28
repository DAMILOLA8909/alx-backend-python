from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    last_edited = models.DateTimeField(null=True, blank=True)
    
    # Self-referential foreign key for threaded conversations
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True,
        verbose_name='Parent Message'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['parent_message', 'timestamp']),
            models.Index(fields=['sender', 'receiver', 'timestamp']),
        ]
    
    def __str__(self):
        if self.parent_message:
            return f"Reply from {self.sender} to {self.receiver} (Thread: {self.parent_message.id})"
        return f"Message from {self.sender} to {self.receiver}"
    
    def get_thread_depth(self):
        """Calculate how deep this message is in the thread"""
        depth = 0
        current = self
        while current.parent_message:
            depth += 1
            current = current.parent_message
        return depth
    
    def get_conversation_root(self):
        """Get the root message of this conversation thread"""
        current = self
        while current.parent_message:
            current = current.parent_message
        return current
    
    @property
    def is_root_message(self):
        """Check if this is a root message (not a reply)"""
        return self.parent_message is None

class MessageHistory(models.Model):
    """Model to store historical versions of edited messages"""
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='history'
    )
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='message_edits'
    )
    edited_at = models.DateTimeField(default=timezone.now)
    edit_reason = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = "Message histories"
    
    def __str__(self):
        return f"History for Message {self.message.id} edited by {self.edited_by}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('reply', 'New Reply'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES, 
        default='message'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user}: {self.message}"