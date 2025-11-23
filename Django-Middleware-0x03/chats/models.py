import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Custom User Manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    class Role(models.TextChoices):
        GUEST = 'guest', _('Guest')
        HOST = 'host', _('Host')
        ADMIN = 'admin', _('Admin')
    
    # Use custom manager
    objects = UserManager()
    
    # Override the default id field to use UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    
    # Remove username field, we'll use email as the primary identifier
    username = None
    
    # Custom fields based on specification
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    password = models.CharField(_('password'), max_length=128)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Set email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_user_email'),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """
    Conversation model to track which users are involved in a conversation
    """
    # Use exact field name from specification
    conversation_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation'
        indexes = [
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        participants = self.participants.all()[:3]
        participant_names = [str(user.user) for user in participants]
        return f"Conversation {self.conversation_id} - Participants: {', '.join(participant_names)}"


class ConversationParticipant(models.Model):
    """
    Junction table to manage many-to-many relationship between Conversation and User
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='participants'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='conversations'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation_participant'
        constraints = [
            models.UniqueConstraint(
                fields=['conversation', 'user'], 
                name='unique_conversation_participant'
            )
        ]
        indexes = [
            models.Index(fields=['conversation', 'user']),
        ]


class Message(models.Model):
    """
    Message model containing sender and conversation information
    """
    # Use exact field name from specification
    message_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        db_index=True
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages',
        null=True,  # Temporary for migration
        blank=True  # Temporary for migration
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['conversation']),
            models.Index(fields=['sent_at']),
            models.Index(fields=['conversation', 'sent_at']),
        ]
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message {self.message_id} from {self.sender} in {self.conversation.conversation_id}"