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

def get_queryset(self):
    user = self.request.user

    if user.role in ['MANAGER', 'EQUIPMENT_MANAGER', 'ADMIN']:
        queryset = Rental.objects.all()
    else:
        queryset = Rental.objects.filter(
            customer=user
        )

    status = self.request.query_params.get('status')
    machine = self.request.query_params.get('machine')
    start_date = self.request.query_params.get('start_date')
    end_date = self.request.query_params.get('end_date')

    if status:
        queryset = queryset.filter(status=status)

    if machine:
        queryset = queryset.filter(machine_id=machine)

    if start_date:
        queryset = queryset.filter(start_date__gte=start_date)

    if end_date:
        queryset = queryset.filter(end_date__lte=end_date)

    return queryset