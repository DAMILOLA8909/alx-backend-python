# chats/middleware.py
import datetime
import os
from django.conf import settings
from django.http import HttpResponseForbidden

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

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get current server time
        current_time = datetime.datetime.now().time()
        
        # Define restricted hours (9 PM to 6 AM)
        start_restriction = datetime.time(21, 0)  # 9:00 PM
        end_restriction = datetime.time(6, 0)     # 6:00 AM
        
        # Check if current time is within restricted hours
        if (current_time >= start_restriction) or (current_time <= end_restriction):
            # Return 403 Forbidden if accessing during restricted hours
            return HttpResponseForbidden(
                "Access denied: The messaging app is only available from 6:00 AM to 9:00 PM."
            )
        
        # If not restricted hours, process the request normally
        response = self.get_response(request)
        return response