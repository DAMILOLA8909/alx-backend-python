from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.utils import timezone

class MessageNotificationTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(
            username='sender', 
            password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver', 
            password='testpass123'
        )
    
    def test_message_creation(self):
        """Test that a message can be created"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message!"
        )
        
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, "Hello, this is a test message!")
        self.assertFalse(message.is_read)
        self.assertFalse(message.edited)
        self.assertIsNone(message.last_edited)
    
    def test_notification_auto_creation(self):
        """Test that notification is automatically created when message is saved"""
        # Count initial notifications
        initial_count = Notification.objects.count()
        
        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message for notification"
        )
        
        # Check if notification was created
        final_count = Notification.objects.count()
        self.assertEqual(final_count, initial_count + 1)
        
        # Verify notification details
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'message')
        self.assertFalse(notification.is_read)
    
    def test_message_edit_tracking(self):
        """Test that message edits are tracked in MessageHistory"""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message content"
        )
        
        # Edit the message content
        original_content = message.content
        message.content = "Edited message content"
        message.save()
        
        # Check that edit was tracked
        self.assertTrue(message.edited)
        self.assertIsNotNone(message.last_edited)
        
        # Check that history entry was created
        history_entries = MessageHistory.objects.filter(message=message)
        self.assertEqual(history_entries.count(), 1)
        
        history_entry = history_entries.first()
        self.assertEqual(history_entry.old_content, original_content)
        self.assertEqual(history_entry.edited_by, self.sender)
    
    def test_multiple_edits_tracked(self):
        """Test that multiple edits create multiple history entries"""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="First version"
        )
        
        # Make multiple edits
        message.content = "Second version"
        message.save()
        
        message.content = "Third version"
        message.save()
        
        message.content = "Fourth version"
        message.save()
        
        # Check that all edits were tracked
        self.assertEqual(MessageHistory.objects.filter(message=message).count(), 3)
        self.assertTrue(message.edited)
    
    def test_no_history_for_new_messages(self):
        """Test that new messages don't create history entries"""
        initial_history_count = MessageHistory.objects.count()
        
        # Create a new message
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Brand new message"
        )
        
        # No history should be created for new messages
        self.assertEqual(MessageHistory.objects.count(), initial_history_count)