from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

@login_required
def delete_user_account(request):
    """
    View to allow users to delete their own account
    """
    if request.method == 'POST':
        # Verify the user is deleting their own account
        if request.user.is_authenticated:
            user_to_delete = request.user
            
            # Log out the user before deletion
            logout(request)
            
            # Delete the user account
            # This will trigger the post_delete signal for cleanup
            user_to_delete.delete()
            
            # Success message (will be shown after redirect)
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('messaging:home')  # Use namespaced URL
        else:
            return HttpResponseForbidden("You are not authorized to perform this action.")
    
    # GET request - show confirmation page
    return render(request, 'delete_account_confirm.html')

def home(request):
    """
    Simple home view for redirect after account deletion
    """
    return render(request, 'home.html')

def home(request):
    """
    Simple home view for redirect after account deletion
    """
    return render(request, 'home.html')