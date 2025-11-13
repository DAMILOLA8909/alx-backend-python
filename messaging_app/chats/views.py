from rest_framework import viewsets, status, filters  # Added filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # Add this import
from django.db.models import Q
from .models import User, Conversation, ConversationParticipant, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    ConversationCreateSerializer,
    ConversationSummarySerializer,
    MessageSerializer,
    MessageCreateSerializer,
    MessageSummarySerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations
    """
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]  # Added filters
    search_fields = ['participants__user__first_name', 'participants__user__last_name']  # Added search
    ordering_fields = ['created_at']  # Added ordering
    ordering = ['-created_at']  # Default ordering
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action
        """
        if self.action == 'create':
            return ConversationCreateSerializer
        elif self.action == 'list':
            return ConversationSummarySerializer
        return ConversationSerializer
    
    def get_queryset(self):
        """
        Return conversations where the current user is a participant
        """
        user = self.request.user
        return Conversation.objects.filter(
            participants__user=user
        ).distinct()

    # ... rest of the ConversationViewSet remains the same ...

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages
    """
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]  # Added filters
    search_fields = ['message_body']  # Added search
    ordering_fields = ['sent_at']  # Added ordering
    ordering = ['-sent_at']  # Default ordering
    filterset_fields = ['conversation__conversation_id', 'sender__user_id']  # Added filtering
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action
        """
        if self.action == 'create':
            return MessageCreateSerializer
        elif self.action == 'list':
            return MessageSummarySerializer
        return MessageSerializer
    
    def get_queryset(self):
        """
        Return messages for conversations where the current user is a participant
        """
        user = self.request.user
        return Message.objects.filter(
            conversation__participants__user=user
        ).distinct()

    # ... rest of the MessageViewSet remains the same ...

# UserViewSet remains the same ...