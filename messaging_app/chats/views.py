from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    # In chats/views.py, update the perform_create method:
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(sender=self.request.user)
        else:
            # Handle unauthenticated user appropriately
            pass

class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer