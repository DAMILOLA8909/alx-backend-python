import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    """
    Filter for messages to retrieve conversations with specific users or within time ranges
    """
    # Filter by conversation with specific user (by user_id)
    participant = filters.UUIDFilter(
        field_name='conversation__participants__user__user_id',
        label='Filter by participant user ID'
    )
    
    # Filter by participant email
    participant_email = filters.CharFilter(
        field_name='conversation__participants__user__email',
        lookup_expr='iexact',
        label='Filter by participant email'
    )
    
    # Filter by time range
    sent_after = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        label='Messages sent after this date/time'
    )
    
    sent_before = filters.DateTimeFilter(
        field_name='sent_at', 
        lookup_expr='lte',
        label='Messages sent before this date/time'
    )
    
    # Filter by sender
    sender = filters.UUIDFilter(
        field_name='sender__user_id',
        label='Filter by sender user ID'
    )
    
    # Filter by conversation
    conversation = filters.UUIDFilter(
        field_name='conversation__conversation_id',
        label='Filter by conversation ID'
    )
    
    # Search in message body
    search = filters.CharFilter(
        field_name='message_body',
        lookup_expr='icontains',
        label='Search in message content'
    )

    class Meta:
        model = Message
        fields = [
            'participant',
            'participant_email', 
            'sent_after',
            'sent_before',
            'sender',
            'conversation',
            'search'
        ]