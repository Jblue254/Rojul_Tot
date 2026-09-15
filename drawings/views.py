from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsArchitecturalManagerOrAdmin

from .models import Drawing, DrawingCategory
from .serializers import (
    DrawingSerializer,
    DrawingCategorySerializer,
)


class DrawingCategoryListCreateView(generics.ListCreateAPIView):
    queryset = DrawingCategory.objects.all().order_by('name')
    serializer_class = DrawingCategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]


class DrawingCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DrawingCategory.objects.all()
    serializer_class = DrawingCategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]


class DrawingListCreateView(generics.ListCreateAPIView):
    serializer_class = DrawingSerializer

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
                category_id=category
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

        return queryset.order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]


class DrawingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]