from django.urls import path
from .views import MessageListCreateAPIView, MessageDetailAPIView

urlpatterns = [
    path('api/messages/', MessageListCreateAPIView.as_view(), name='message_list_create'),
    path('api/messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message_detail'),
]