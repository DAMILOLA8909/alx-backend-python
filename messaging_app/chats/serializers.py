from rest_framework import serializers
from .models import User, Conversation, ConversationParticipant, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
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
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        for user_id in participant_ids:
            try:
                user = User.objects.get(user_id=user_id)
                ConversationParticipant.objects.create(
                    conversation=conversation,
                    user=user
                )
            except User.DoesNotExist:
                # Skip invalid user IDs or handle error as needed
                continue
        
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages
    """
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
    
    def create(self, validated_data):
        # In a real application, you might want to set the sender automatically
        # from the request user
        return Message.objects.create(**validated_data)

# Simplified serializers for basic operations
class UserSummarySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for user summary (used in nested relationships)
    """
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']

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
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender_summary', 'message_body', 'sent_at']