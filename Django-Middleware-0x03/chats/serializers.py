from rest_framework import serializers
from django.core.validators import validate_email, RegexValidator
from .models import User, Conversation, ConversationParticipant, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    # Add explicit CharField with validation
    first_name = serializers.CharField(
        max_length=150,
        required=True,
        error_messages={'required': 'First name is required'}
    )
    last_name = serializers.CharField(
        max_length=150,
        required=True,
        error_messages={'required': 'Last name is required'}
    )
    email = serializers.CharField(
        validators=[validate_email],
        error_messages={'invalid': 'Enter a valid email address'}
    )
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    
    class Meta:
        model = User
        fields = [
            'user_id', 
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'role', 
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_email(self, value):
        """Custom email validation"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_role(self, value):
        """Custom role validation"""
        valid_roles = [choice[0] for choice in User.Role.choices]
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role must be one of: {', '.join(valid_roles)}")
        return value
    
    def create(self, validated_data):
        """Create a new user with encrypted password"""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update a user, handling password properly"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ConversationParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation Participants
    """
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = ConversationParticipant
        fields = ['id', 'user', 'user_details', 'joined_at']
        read_only_fields = ['id', 'joined_at']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender_details = UserSerializer(source='sender', read_only=True)
    message_body = serializers.CharField(
        required=True,
        error_messages={'required': 'Message body is required'},
        style={'base_template': 'textarea.html'}
    )
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_details',
            'conversation',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender_details']
    
    def validate_message_body(self, value):
        """Validate message body is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Message body is too short.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested relationships
    """
    participants_details = ConversationParticipantSerializer(
        source='participants', 
        many=True, 
        read_only=True
    )
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants_details',
            'messages',
            'participant_count',
            'last_message',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_participant_count(self, obj):
        """Get the number of participants in the conversation"""
        return obj.participants.count()
    
    def get_last_message(self, obj):
        """Get the most recent message in the conversation"""
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating conversations with participants
    """
    participant_ids = serializers.ListField(
        child=serializers.CharField(),  # Using CharField for UUID strings
        write_only=True,
        required=True,
        error_messages={'required': 'At least one participant ID is required'}
    )
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def validate_participant_ids(self, value):
        """Validate that participant IDs exist and are valid"""
        if not value:
            raise serializers.ValidationError("At least one participant is required.")
        
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        
        # Check if all user IDs exist
        valid_users = User.objects.filter(user_id__in=value)
        if len(valid_users) != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid.")
        
        return value
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        for user_id in participant_ids:
            user = User.objects.get(user_id=user_id)
            ConversationParticipant.objects.create(
                conversation=conversation,
                user=user
            )
        
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages
    """
    message_body = serializers.CharField(
        required=True,
        error_messages={'required': 'Message body is required'}
    )
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
    
    def validate(self, data):
        """Validate message creation"""
        # Check if sender is a participant in the conversation
        conversation = data.get('conversation')
        sender = data.get('sender')
        
        if conversation and sender:
            is_participant = ConversationParticipant.objects.filter(
                conversation=conversation,
                user=sender
            ).exists()
            
            if not is_participant:
                raise serializers.ValidationError(
                    "Sender must be a participant in the conversation."
                )
        
        return data
    
    def create(self, validated_data):
        return Message.objects.create(**validated_data)

# Simplified serializers for basic operations
class UserSummarySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for user summary
    """
    name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'name', 'email']

class ConversationSummarySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for conversation summary
    """
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'created_at']

class MessageSummarySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for message summary
    """
    sender_summary = UserSummarySerializer(source='sender', read_only=True)
    message_preview = serializers.CharField(source='get_message_preview', read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender_summary', 'message_preview', 'sent_at']