from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import IsManagerOrAdmin

from machinery.models import Machine

from notifications.models import Notification
from notifications.utils import create_notification

from .models import Rental
from .serializers import RentalSerializer


STAFF_ROLES = [
    User.Role.ADMIN,
    User.Role.MANAGER,
    User.Role.EQUIPMENT_MANAGER,
]


def notify_staff(title, message):
    """Send one notification to every staff user (each user once)."""
    for staff_user in User.objects.filter(role__in=STAFF_ROLES):
        create_notification(
            recipient=staff_user,
            title=title,
            message=message,
            notification_type=Notification.NotificationType.RENTAL,
        )


def process_expired_rentals():
    today = timezone.now().date()

    expired_rentals = Rental.objects.select_related(
        "customer", "machine"
    ).filter(
        end_date__lt=today,
        status=Rental.Status.ACTIVE,
    )

    for rental in expired_rentals:
        with transaction.atomic():
            rental.status = Rental.Status.COMPLETED
            rental.save()

            rental.machine.status = Machine.Status.AVAILABLE
            rental.machine.save()

            # Customer
            create_notification(
                recipient=rental.customer,
                title="Rental Completed",
                message=(
                    f"Rental for {rental.machine.name} "
                    f"has been completed."
                ),
                notification_type=Notification.NotificationType.RENTAL,
            )

            # Staff (admins, managers, equipment managers)
            notify_staff(
                title="Rental Auto Completed",
                message=(
                    f"Rental #{rental.id} for {rental.machine.name} "
                    f"has been automatically completed."
                ),
            )


def rentals_for_user(user):
    if user.role in STAFF_ROLES:
        return Rental.objects.all()
    return Rental.objects.filter(customer=user)


class RentalListCreateView(generics.ListCreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        process_expired_rentals()

        queryset = rentals_for_user(self.request.user)
        params = self.request.query_params

        status_param = params.get("status")
        machine = params.get("machine")
        start_date = params.get("start_date")
        end_date = params.get("end_date")

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
        process_expired_rentals()
        return rentals_for_user(self.request.user)


class RentalActionView(APIView):
    """Base class for approve / reject / activate / complete actions."""

    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    new_status = None
    machine_status = None  # set to update the machine too
    title = ""
    success_message = ""

    def build_message(self, rental):
        raise NotImplementedError

    @transaction.atomic
    def patch(self, request, pk):
        rental = get_object_or_404(
            Rental.objects.select_related("customer", "machine"), pk=pk
        )

        rental.status = self.new_status
        rental.save()

        if self.machine_status is not None:
            rental.machine.status = self.machine_status
            rental.machine.save()

        create_notification(
            recipient=rental.customer,
            title=self.title,
            message=self.build_message(rental),
            notification_type=Notification.NotificationType.RENTAL,
        )

        return Response({"message": self.success_message})


class ApproveRentalView(RentalActionView):
    new_status = Rental.Status.APPROVED
    title = "Rental Approved"
    success_message = "Rental approved"

    def build_message(self, rental):
        return (
            f"Your rental request for {rental.machine.name} "
            f"has been approved."
        )


class RejectRentalView(RentalActionView):
    new_status = Rental.Status.REJECTED
    title = "Rental Rejected"
    success_message = "Rental rejected"

    def build_message(self, rental):
        return (
            f"Your rental request for {rental.machine.name} "
            f"has been rejected."
        )


class ActivateRentalView(RentalActionView):
    new_status = Rental.Status.ACTIVE
    machine_status = Machine.Status.RENTED
    title = "Rental Activated"
    success_message = "Rental activated"

    def build_message(self, rental):
        return (
            f"{rental.machine.name} has been handed over and "
            f"the rental is now active."
        )


class CompleteRentalView(RentalActionView):
    new_status = Rental.Status.COMPLETED
    machine_status = Machine.Status.AVAILABLE
    title = "Rental Completed"
    success_message = "Rental completed"

    def build_message(self, rental):
        return f"Rental for {rental.machine.name} has been completed."