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

def get_queryset(self):
    queryset = Drawing.objects.all()

    search = self.request.query_params.get('search')
    category = self.request.query_params.get('category')
    status = self.request.query_params.get('status')
    min_price = self.request.query_params.get('min_price')
    max_price = self.request.query_params.get('max_price')

    if search:
        queryset = queryset.filter(
            title__icontains=search
        ) | queryset.filter(
            description__icontains=search
        )

    if category:
        queryset = queryset.filter(
            category__icontains=category
        )

    if status:
        queryset = queryset.filter(
            status=status
        )

    if min_price:
        queryset = queryset.filter(
            price__gte=min_price
        )

    if max_price:
        queryset = queryset.filter(
            price__lte=max_price
        )

    return queryset