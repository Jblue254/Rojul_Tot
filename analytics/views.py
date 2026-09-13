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
from accounts.models import User


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

class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        data = {
            "total_users": User.objects.count(),
            "customers": User.objects.filter(
                role=User.Role.CUSTOMER
            ).count(),
            "managers": User.objects.filter(
                role=User.Role.MANAGER
            ).count(),
            "equipment_managers": User.objects.filter(
                role=User.Role.EQUIPMENT_MANAGER
            ).count(),
            "admins": User.objects.filter(
                role=User.Role.ADMIN
            ).count(),
            "active_users": User.objects.filter(
                is_active=True
            ).count(),
        }

        return Response(data)
class RentalOrderStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request):
        rental_revenue = Rental.objects.filter(
            status__in=[
                Rental.Status.APPROVED,
                Rental.Status.ACTIVE,
                Rental.Status.COMPLETED,
            ]
        ).aggregate(
            total=Sum("total_price")
        )["total"] or 0

        order_revenue = Order.objects.filter(
            status__in=[
                Order.Status.PAID,
                Order.Status.PROCESSING,
                Order.Status.COMPLETED,
            ]
        ).aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        data = {
            "rentals": {
                "total": Rental.objects.count(),
                "pending": Rental.objects.filter(
                    status=Rental.Status.PENDING
                ).count(),
                "approved": Rental.objects.filter(
                    status=Rental.Status.APPROVED
                ).count(),
                "active": Rental.objects.filter(
                    status=Rental.Status.ACTIVE
                ).count(),
                "completed": Rental.objects.filter(
                    status=Rental.Status.COMPLETED
                ).count(),
                "cancelled": Rental.objects.filter(
                    status=Rental.Status.CANCELLED
                ).count(),
                "revenue": rental_revenue,
            },

            "orders": {
                "total": Order.objects.count(),
                "pending": Order.objects.filter(
                    status=Order.Status.PENDING
                ).count(),
                "paid": Order.objects.filter(
                    status=Order.Status.PAID
                ).count(),
                "processing": Order.objects.filter(
                    status=Order.Status.PROCESSING
                ).count(),
                "completed": Order.objects.filter(
                    status=Order.Status.COMPLETED
                ).count(),
                "cancelled": Order.objects.filter(
                    status=Order.Status.CANCELLED
                ).count(),
                "revenue": order_revenue,
            },

            "combined_revenue": rental_revenue + order_revenue,
        }

        return Response(data)