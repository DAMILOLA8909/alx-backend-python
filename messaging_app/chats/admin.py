from django.contrib import admin
from .models import User, Conversation, ConversationParticipant, Message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'phone_number', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'get_participants_count']
    list_filter = ['created_at']
    search_fields = ['id', 'participants__email', 'participants__first_name']
    ordering = ['-created_at']
    
    def get_participants_count(self, obj):
        return obj.participants.count()
    get_participants_count.short_description = 'Participants Count'

@admin.register(ConversationParticipant)
class ConversationParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'user', 'joined_at']
    list_filter = ['joined_at']
    search_fields = ['conversation__id', 'user__email', 'user__first_name']
    ordering = ['-joined_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'conversation', 'sent_at', 'get_message_preview']
    list_filter = ['sent_at', 'conversation']
    search_fields = [
        'message_body', 
        'sender__email', 
        'sender__first_name',
        'conversation__id'
    ]
    ordering = ['-sent_at']
    
    def get_message_preview(self, obj):
        """Display a shortened version of the message body"""
        if len(obj.message_body) > 50:
            return f"{obj.message_body[:50]}..."
        return obj.message_body
    get_message_preview.short_description = 'Message Preview'