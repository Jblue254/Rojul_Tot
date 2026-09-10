from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Drawing
from .serializers import DrawingSerializer


class DrawingListCreateView(generics.ListCreateAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DrawingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]