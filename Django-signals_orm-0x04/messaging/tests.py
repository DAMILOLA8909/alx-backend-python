from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.utils import timezone
from django.urls import reverse

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
    
    def test_user_deletion_cleanup(self):
        """Test that user deletion properly cleans up related data"""
        # Create a user and some related data
        user_to_delete = User.objects.create_user(
            username='user_to_delete', 
            password='testpass123'
        )
        other_user = User.objects.create_user(
            username='other_user', 
            password='testpass123'
        )
        
        # Create messages sent by and received by the user
        sent_message = Message.objects.create(
            sender=user_to_delete,
            receiver=other_user,
            content="Message sent by user to be deleted"
        )
        received_message = Message.objects.create(
            sender=other_user,
            receiver=user_to_delete,
            content="Message received by user to be deleted"
        )
        
        # Create notifications for the user
        notification = Notification.objects.create(
            user=user_to_delete,
            message=received_message,
            notification_type='message'
        )
        
        # Create message history for edits by the user
        history_entry = MessageHistory.objects.create(
            message=sent_message,
            old_content="Original content",
            edited_by=user_to_delete,
            edit_reason="Test edit"
        )
        
        # Record counts before deletion
        initial_user_count = User.objects.count()
        initial_message_count = Message.objects.count()
        initial_notification_count = Notification.objects.count()
        initial_history_count = MessageHistory.objects.count()
        
        # Store the user ID for later querying
        user_id = user_to_delete.id
        
        # Delete the user
        user_to_delete.delete()
        
        # Verify user was deleted
        self.assertEqual(User.objects.count(), initial_user_count - 1)
        
        # Verify related data was cleaned up
        # Use the stored user_id instead of the deleted user instance
        self.assertFalse(Message.objects.filter(sender_id=user_id).exists())
        self.assertFalse(Message.objects.filter(receiver_id=user_id).exists())
        self.assertFalse(Notification.objects.filter(user_id=user_id).exists())
        self.assertFalse(MessageHistory.objects.filter(edited_by_id=user_id).exists())
    
    def test_delete_account_view(self):
        """Test the delete account view"""
        # Create and login a user
        user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Access the delete account page
        response = self.client.get(reverse('messaging:delete_account'))
        self.assertEqual(response.status_code, 200)
        
        # Submit the delete form
        response = self.client.post(reverse('messaging:delete_account'))
        
        # Should redirect to home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('messaging:home'))
        
        # Verify user was deleted
        self.assertFalse(User.objects.filter(username='testuser').exists())
    
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