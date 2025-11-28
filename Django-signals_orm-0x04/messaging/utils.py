from django.db.models import Prefetch, Q
from .models import Message

def get_threaded_messages_optimized(user, other_user=None, message_id=None):
    """
    Get threaded conversations with optimized queries using prefetch_related and select_related
    """
    # Base queryset with select_related to reduce database hits
    base_query = Message.objects.select_related(
        'sender', 
        'receiver', 
        'parent_message'
    ).filter(
        sender=user
    ) | Message.objects.select_related(
        'sender', 
        'receiver', 
        'parent_message'
    ).filter(
        receiver=user
    )
    
    if other_user:
        # Get conversation between two specific users
        base_query = base_query.filter(
            Q(sender=user, receiver=other_user) |
            Q(sender=other_user, receiver=user)
        )
    
    if message_id:
        # Get specific thread
        base_query = base_query.filter(
            Q(id=message_id) |
            Q(parent_message_id=message_id) |
            Q(parent_message__parent_message_id=message_id)
        )
    
    # Prefetch replies recursively (up to 5 levels deep for practical purposes)
    prefetch_replies = Prefetch(
        'replies',
        queryset=Message.objects.select_related('sender', 'receiver')
                   .prefetch_related('replies')
                   .all(),
        to_attr='direct_replies'
    )
    
    # Get root messages (messages without parents)
    root_messages = base_query.filter(parent_message__isnull=True)\
                              .prefetch_related(prefetch_replies)\
                              .order_by('-timestamp')
    
    return root_messages

def build_thread_tree(messages):
    """
    Build a hierarchical thread structure from flat message list
    """
    def build_tree(message, depth=0):
        tree_node = {
            'message': message,
            'depth': depth,
            'replies': []
        }
        
        # Recursively build tree for replies
        if hasattr(message, 'direct_replies'):
            for reply in message.direct_replies:
                tree_node['replies'].append(build_tree(reply, depth + 1))
        
        return tree_node
    
    thread_trees = []
    for message in messages:
        thread_trees.append(build_tree(message))
    
    return thread_trees

def get_message_thread(message_id):
    """
    Get complete thread for a specific message
    """
    # Get the root message and all its descendants
    try:
        root_message = Message.objects.get(id=message_id)
        if root_message.parent_message:
            root_message = root_message.get_conversation_root()
        
        # Get all messages in the thread
        thread_messages = Message.objects.filter(
            Q(id=root_message.id) |
            Q(parent_message=root_message.id) |
            Q(parent_message__parent_message=root_message.id) |
            Q(parent_message__parent_message__parent_message=root_message.id) |
            Q(parent_message__parent_message__parent_message__parent_message=root_message.id)
        ).select_related('sender', 'receiver', 'parent_message')\
         .order_by('timestamp')
        
        return build_thread_tree([root_message])
    
    except Message.DoesNotExist:
        return []