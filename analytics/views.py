from django.db.models import Avg, Count, Sum
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from machinery.models import Machine
from rentals.models import Rental
from drawings.models import Drawing
from orders.models import Order
from projects.models import Project
from reviews.models import Review
from accounts.permissions import IsAdmin, IsManagerOrAdmin


class DashboardStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request):
        data = {
            "machinery": {
                "total": Machine.objects.count(),
                "available": Machine.objects.filter(
                    status=Machine.Status.AVAILABLE
                ).count(),
                "rented": Machine.objects.filter(
                    status=Machine.Status.RENTED
                ).count(),
                "maintenance": Machine.objects.filter(
                    status=Machine.Status.MAINTENANCE
                ).count(),
            },

            "rentals": {
                "total": Rental.objects.count(),
                "pending": Rental.objects.filter(
                    status=Rental.Status.PENDING
                ).count(),
                "active": Rental.objects.filter(
                    status=Rental.Status.ACTIVE
                ).count(),
                "completed": Rental.objects.filter(
                    status=Rental.Status.COMPLETED
                ).count(),
            },

            "drawings": {
                "total": Drawing.objects.count(),
                "available": Drawing.objects.filter(
                    status=Drawing.Status.AVAILABLE
                ).count(),
            },

            "orders": {
                "total": Order.objects.count(),
                "pending": Order.objects.filter(
                    status=Order.Status.PENDING
                ).count(),
                "completed": Order.objects.filter(
                    status=Order.Status.COMPLETED
                ).count(),
                "revenue": Order.objects.filter(
                    status__in=[
                        Order.Status.PAID,
                        Order.Status.PROCESSING,
                        Order.Status.COMPLETED,
                    ]
                ).aggregate(
                    total=Sum("total_amount")
                )["total"] or 0,
            },

            "projects": {
                "total": Project.objects.count(),
                "active": Project.objects.filter(
                    status=Project.Status.ACTIVE
                ).count(),
                "completed": Project.objects.filter(
                    status=Project.Status.COMPLETED
                ).count(),
            },

            "reviews": {
                "total": Review.objects.count(),
                "average_rating": Review.objects.aggregate(
                    average=Avg("rating")
                )["average"] or 0,
            },
        }

        return Response(data)