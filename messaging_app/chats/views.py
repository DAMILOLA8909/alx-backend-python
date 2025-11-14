from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
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

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_root(request):
    return HttpResponse("""
    <h1>Messaging App API</h1>
    <ul>
        <li><a href="/api/conversations/">Conversations API</a></li>
        <li><a href="/api/messages/">Messages API</a></li>
        <li><a href="/api/users/">Users API</a></li>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/api-auth/login/">Login</a></li>
    </ul>
    """)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations
    """
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['participants__user__first_name', 'participants__user__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
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
    
    def list(self, request, *args, **kwargs):
        """
        List conversations for the authenticated user
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ensure the current user is included in participants
        participant_ids = serializer.validated_data.get('participant_ids', [])
        if str(request.user.user_id) not in participant_ids:
            participant_ids.append(str(request.user.user_id))
        
        conversation = serializer.save()
        
        # Return the full conversation details
        full_serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(full_serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific conversation with all messages
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Custom action to get messages for a specific conversation
        """
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('sent_at')
        
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Custom action to add a participant to an existing conversation
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user is already a participant
        if ConversationParticipant.objects.filter(conversation=conversation, user=user).exists():
            return Response(
                {'error': 'User is already a participant'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add user to conversation
        ConversationParticipant.objects.create(conversation=conversation, user=user)
        
        return Response(
            {'message': 'Participant added successfully'}, 
            status=status.HTTP_200_OK
        )

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages
    """
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    filterset_fields = ['conversation__conversation_id', 'sender__user_id']
    
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
    
    def list(self, request, *args, **kwargs):
        """
        List messages for the authenticated user
        """
        queryset = self.get_queryset()
        
        # Filter by conversation if provided
        conversation_id = request.query_params.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id)
                # Verify user is a participant in this conversation
                if not ConversationParticipant.objects.filter(
                    conversation=conversation, user=request.user
                ).exists():
                    return Response(
                        {'error': 'Access denied to this conversation'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                queryset = queryset.filter(conversation=conversation)
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new message in a conversation
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set the sender to the current user
        validated_data = serializer.validated_data
        validated_data['sender'] = request.user
        
        # Verify user is a participant in the conversation
        conversation = validated_data.get('conversation')
        if not ConversationParticipant.objects.filter(
            conversation=conversation, user=request.user
        ).exists():
            return Response(
                {'error': 'You are not a participant in this conversation'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        message = serializer.save()
        
        # Return the full message details
        full_serializer = MessageSerializer(message, context={'request': request})
        return Response(full_serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific message
        """
        instance = self.get_object()
        
        # Verify user has access to this message
        if not ConversationParticipant.objects.filter(
            conversation=instance.conversation, user=request.user
        ).exists():
            return Response(
                {'error': 'Access denied to this message'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing users (read-only)
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Changed from UserSummarySerializer to UserSerializer
    
    def get_queryset(self):
        """
        Return all users except the current user
        """
        return User.objects.exclude(user_id=self.request.user.user_id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Custom action to get current user details
        """
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)