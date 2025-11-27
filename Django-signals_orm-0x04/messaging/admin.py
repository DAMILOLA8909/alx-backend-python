from django.contrib import admin
from .models import Message, Notification, MessageHistory

class MessageHistoryInline(admin.TabularInline):
    """Inline display of message history in Message admin"""
    model = MessageHistory
    extra = 0
    readonly_fields = ['edited_by', 'edited_at', 'old_content']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False  # Prevent adding history entries manually

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp', 'is_read', 'edited', 'last_edited']
    list_filter = ['timestamp', 'is_read', 'edited', 'last_edited']
    search_fields = ['sender__username', 'receiver__username', 'content']
    date_hierarchy = 'timestamp'
    readonly_fields = ['last_edited']
    inlines = [MessageHistoryInline]
    
    fieldsets = (
        ('Message Details', {
            'fields': ('sender', 'receiver', 'content', 'is_read', 'edited')
        }),
        ('Timestamps', {
            'fields': ('timestamp', 'last_edited'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ['message', 'edited_by', 'edited_at']
    list_filter = ['edited_at']
    search_fields = ['message__content', 'old_content', 'edited_by__username']
    date_hierarchy = 'edited_at'
    readonly_fields = ['message', 'old_content', 'edited_by', 'edited_at']
    
    fieldsets = (
        ('Edit Information', {
            'fields': ('message', 'edited_by', 'edit_reason')
        }),
        ('Content History', {
            'fields': ('old_content',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('edited_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation of history entries

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'message__content']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('user', 'message', 'notification_type', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )