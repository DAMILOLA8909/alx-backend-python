from django.urls import path, include  # Added include
from rest_framework import routers  # Added routers
from .views import ConversationViewSet, MessageViewSet, UserViewSet

# Create a router and register our viewsets
router = routers.DefaultRouter()  # Using DefaultRouter
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),  # Include router URLs under api/
]