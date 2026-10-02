from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateView(
    generics.CreateAPIView
):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


class ContactMessageListView(
    generics.ListAPIView
):
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactMessage.objects.all().order_by(
            "-created_at"
        )


class ContactMessageDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContactMessage.objects.all()