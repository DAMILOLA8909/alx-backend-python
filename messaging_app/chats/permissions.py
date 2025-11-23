from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or conversation participants to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if user is the owner of the object
        if hasattr(obj, 'sender') and obj.sender == request.user:
            return True
        
        # Check if user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user=request.user).exists()
        
        # For user objects, allow users to access their own data
        if hasattr(obj, 'user_id') and obj.user_id == request.user.user_id:
            return True
            
        return False


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(user=request.user).exists()


class IsMessageParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.conversation.participants.filter(user=request.user).exists()


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.user_id