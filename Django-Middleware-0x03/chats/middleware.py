# chats/middleware.py
import datetime
import os
from django.conf import settings

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = 'requests.log'
        
    def __call__(self, request):
        # Get user information
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        else:
            user = "Anonymous"
        
        # Create log entry with timestamp
        timestamp = datetime.datetime.now()
        log_entry = f"{timestamp} - User: {user} - Path: {request.path}\n"
        
        # Write to log file (append mode)
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            # Fallback to console if file writing fails
            print(f"Failed to write to log file: {e}")
            print(log_entry)
        
        # Process the request and return response
        response = self.get_response(request)
        return response