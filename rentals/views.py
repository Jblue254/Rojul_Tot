from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import IsManagerOrAdmin
from notifications.models import Notification
from machinery.models import Machine
from .models import Rental
from .serializers import RentalSerializer


class RentalListCreateView(generics.ListCreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'EQUIPMENT_MANAGER', 'ADMIN']:
            queryset = Rental.objects.all()
        else:
            queryset = Rental.objects.filter(customer=user)

        # Query parameter filters
        status_param = self.request.query_params.get('status')
        machine = self.request.query_params.get('machine')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if machine:
            queryset = queryset.filter(machine_id=machine)

        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        return queryset

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


class ApproveRentalView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def patch(self, request, pk):
        rental = Rental.objects.get(pk=pk)

        rental.status = Rental.Status.APPROVED
        rental.save()

        Notification.objects.create(
            recipient=rental.customer,
            title="Rental Approved",
            message=f"Your rental request for {rental.machine.name} has been approved."
        )

        return Response({
            "message": "Rental approved"
        })


class RejectRentalView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def patch(self, request, pk):
        rental = Rental.objects.get(pk=pk)

        rental.status = Rental.Status.REJECTED
        rental.save()

        Notification.objects.create(
            recipient=rental.customer,
            title="Rental Rejected",
            message=f"Your rental request for {rental.machine.name} has been rejected."
        )

        return Response({
            "message": "Rental rejected"
        })

class CompleteRentalView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def patch(self, request, pk):
        rental = Rental.objects.get(pk=pk)

        rental.status = Rental.Status.COMPLETED
        rental.save()

        rental.machine.status = Machine.Status.AVAILABLE
        rental.machine.save()

        Notification.objects.create(
            recipient=rental.customer,
            title="Rental Completed",
            message=f"Rental for {rental.machine.name} has been completed."
        )

        return Response({
            "message": "Rental completed"
        })

class ActivateRentalView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def patch(self, request, pk):
        rental = Rental.objects.get(pk=pk)

        rental.status = Rental.Status.ACTIVE
        rental.save()

        rental.machine.status = Machine.Status.RENTED
        rental.machine.save()

        Notification.objects.create(
            recipient=rental.customer,
            title="Rental Activated",
            message=f"{rental.machine.name} has been handed over and rental is now active."
        )

        return Response({
            "message": "Rental activated"
        })