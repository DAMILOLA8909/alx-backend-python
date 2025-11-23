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
        # For Message objects - check if user is participant in the conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user=request.user).exists()
        
        # For Conversation objects - check if user is a participant
        if hasattr(obj, 'participants'):
            return obj.participants.filter(user=request.user).exists()
            
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner
        return obj.user_id == request.user.user_id


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow message sender to update/delete, 
    and participants to view messages.
    """
    
    def has_object_permission(self, request, view, obj):
        # Participants can view messages
        if request.method in permissions.SAFE_METHODS:
            return obj.conversation.participants.filter(user=request.user).exists()
        
        # Only sender can update or delete messages
        return obj.sender == request.user