from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def perform_create(self, serializer):
        # In a real app, you'd set the sender to the current user
        serializer.save(sender=self.request.user)

class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer