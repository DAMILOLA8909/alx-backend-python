from django.contrib import admin
from django.urls import path, include  # Make sure include is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chats.urls')),  # This will include our API routes
]