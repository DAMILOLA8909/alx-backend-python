from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from chats.views import ConversationViewSet, MessageViewSet, UserViewSet

# Create a router and register our viewsets at the project level
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # API routes at project level
]