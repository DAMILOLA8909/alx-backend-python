import datetime
import os
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from collections import defaultdict

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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts per IP: {ip: [(timestamp1, count), (timestamp2, count), ...]}
        self.request_history = defaultdict(list)
        self.limit = 5  # 5 messages per minute
        self.window = 60  # 1 minute in seconds
        
    def __call__(self, request):
        # Only check POST requests (assuming messages are sent via POST)
        if request.method == 'POST':
            # Get client IP address
            ip = self.get_client_ip(request)
            current_time = datetime.datetime.now()
            
            # Clean old entries (older than 1 minute)
            self.clean_old_entries(ip, current_time)
            
            # Check if IP has exceeded the limit
            if self.is_rate_limited(ip, current_time):
                return HttpResponseForbidden(
                    "Rate limit exceeded: Maximum 5 messages per minute. Please try again later."
                )
            
            # Add current request to history
            self.request_history[ip].append(current_time)
        
        # Process the request normally
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def clean_old_entries(self, ip, current_time):
        """Remove entries older than the time window"""
        cutoff_time = current_time - datetime.timedelta(seconds=self.window)
        self.request_history[ip] = [
            timestamp for timestamp in self.request_history[ip] 
            if timestamp > cutoff_time
        ]
    
    def is_rate_limited(self, ip, current_time):
        """Check if IP has exceeded the rate limit"""
        return len(self.request_history[ip]) >= self.limit

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths that require admin/moderator access
        self.protected_paths = [
            '/admin/',  # Django admin
            '/api/delete/',  # Example: delete messages
            '/api/ban/',  # Example: ban users
            '/api/moderation/',  # Example: moderation actions
        ]
        
    def __call__(self, request):
        # Check if the current path requires special permissions
        if self.requires_permission(request.path):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return HttpResponseForbidden(
                    "Access denied: Authentication required for this action."
                )
            
            # Check if user has admin or moderator role
            if not self.has_permission(request.user):
                return HttpResponseForbidden(
                    "Access denied: Admin or Moderator role required for this action."
                )
        
        # Process the request normally
        response = self.get_response(request)
        return response
    
    def requires_permission(self, path):
        """Check if the requested path requires special permissions"""
        return any(path.startswith(protected_path) for protected_path in self.protected_paths)
    
    def has_permission(self, user):
        """Check if user has admin or moderator role"""
        # Method 1: Check Django's built-in is_staff and is_superuser
        if user.is_superuser or user.is_staff:
            return True
        
        # Method 2: Check custom groups
        if user.groups.filter(name__in=['admin', 'moderator']).exists():
            return True
        
        # Method 3: Check custom user profile field (if exists)
        if hasattr(user, 'profile'):
            if user.profile.role in ['admin', 'moderator']:
                return True
        
        return False