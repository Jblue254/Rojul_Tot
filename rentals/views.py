from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Rental
from .serializers import RentalSerializer


class RentalListCreateView(generics.ListCreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'EQUIPMENT_MANAGER', 'ADMIN']:
            return Rental.objects.all()

        return Rental.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class RentalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'EQUIPMENT_MANAGER', 'ADMIN']:
            return Rental.objects.all()

        return Rental.objects.filter(customer=user)