from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewOwnerOrAdmin


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwnerOrAdmin]

    def get_queryset(self):
        return Review.objects.all()

def get_queryset(self):
    queryset = Review.objects.all()

    machine = self.request.query_params.get('machine')
    drawing = self.request.query_params.get('drawing')
    rating = self.request.query_params.get('rating')

    if machine:
        queryset = queryset.filter(
            machine_id=machine
        )

    if drawing:
        queryset = queryset.filter(
            drawing_id=drawing
        )

    if rating:
        queryset = queryset.filter(
            rating=rating
        )

    return queryset