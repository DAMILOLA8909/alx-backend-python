from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    Allows authenticated users to access the API.
    """
    
    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Allow only participants in a conversation to send, view, update and delete messages
        """
        # Check if user is participant in the conversation
        if hasattr(obj, 'conversation'):
            is_participant = obj.conversation.participants.filter(user=request.user).exists()
            
            # For safe methods (GET, HEAD, OPTIONS) - allow participants
            if request.method in permissions.SAFE_METHODS:
                return is_participant
            
            # For unsafe methods (POST, PUT, PATCH, DELETE) - allow participants
            # POST for sending messages, PUT/PATCH/DELETE for message operations
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return is_participant
        
        # For Conversation objects - check if user is a participant
        if hasattr(obj, 'participants'):
            is_participant = obj.participants.filter(user=request.user).exists()
            
            # Allow participants to view, update, delete conversations
            if request.method in permissions.SAFE_METHODS + ['PUT', 'PATCH', 'DELETE']:
                return is_participant
            
            # POST for creating conversations is handled by has_permission
            
        return False


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow message sender to update/delete, 
    and participants to view messages.
    """
    
    def has_object_permission(self, request, view, obj):
        # Participants can view messages (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return obj.conversation.participants.filter(user=request.user).exists()
        
        # Only sender can update (PUT, PATCH) or delete (DELETE) messages
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender == request.user
        
        # For POST (creating messages) - handled by conversation participant check
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions (PUT, PATCH, DELETE) are only allowed to the owner
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.user_id == request.user.user_id
            
        return False


class CanSendMessage(permissions.BasePermission):
    """
    Custom permission to check if user can send messages in a conversation.
    """
    
    def has_permission(self, request, view):
        # For POST requests (sending messages), check if user is participant
        if request.method == 'POST':
            # This would need additional logic to check conversation participation
            # based on the request data
            return request.user and request.user.is_authenticated
        return True
    
    def has_object_permission(self, request, view, obj):
        # Allow participants to perform any message operation
        if hasattr(obj, 'conversation'):
            is_participant = obj.conversation.participants.filter(user=request.user).exists()
            
            # Allow participants to view, update, delete messages
            if request.method in permissions.SAFE_METHODS + ['PUT', 'PATCH', 'DELETE']:
                return is_participant
        
        return False