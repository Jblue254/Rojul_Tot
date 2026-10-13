
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsArchitecturalManagerOrAdmin
from config.supabase_storage import download_private_file

from .models import Drawing, DrawingCategory
from .serializers import (
    DrawingSerializer,
    DrawingCategorySerializer,
)


class PublicDrawingListView(generics.ListAPIView):
    serializer_class = DrawingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Drawing.objects.filter(
            status=Drawing.Status.AVAILABLE
        ).order_by("-created_at")


class PublicDrawingDetailView(generics.RetrieveAPIView):
    queryset = Drawing.objects.filter(
        status=Drawing.Status.AVAILABLE
    )
    serializer_class = DrawingSerializer
    permission_classes = [AllowAny]


class DrawingCategoryListCreateView(generics.ListCreateAPIView):
    queryset = DrawingCategory.objects.all().order_by("name")
    serializer_class = DrawingCategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]


class DrawingCategoryDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = DrawingCategory.objects.all()
    serializer_class = DrawingCategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]


class DrawingListCreateView(generics.ListCreateAPIView):
    serializer_class = DrawingSerializer

    def get_queryset(self):
        queryset = Drawing.objects.all()

        search = self.request.query_params.get("search")
        category = self.request.query_params.get("category")
        drawing_status = self.request.query_params.get("status")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )

        if category:
            queryset = queryset.filter(category_id=category)

        if drawing_status:
            queryset = queryset.filter(status=drawing_status)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.order_by("-created_at")

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]


class DrawingDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [
            IsAuthenticated(),
            IsArchitecturalManagerOrAdmin(),
        ]


class PurchasedDrawingDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        from orders.models import OrderItem

        # Confirm the authenticated customer has a paid order
        # containing this exact drawing.
        purchased = OrderItem.objects.filter(
            drawing_id=pk,
            order__customer=request.user,
            order__status__in=[
                "PAID",
                "PROCESSING",
                "COMPLETED",
            ],
        ).exists()

        if not purchased:
            raise PermissionDenied(
                "You must purchase this drawing before downloading it."
            )

        drawing = get_object_or_404(Drawing, pk=pk)

        if not drawing.drawing_file:
            raise NotFound("The drawing file is not available.")

        try:
            content = download_private_file(
                "drawing-files",
                drawing.drawing_file.name,
            )
        except Exception:
            return Response(
                {"detail": "Could not retrieve the drawing file."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        response = HttpResponse(
            content,
            content_type="application/pdf",
        )
        response["Content-Disposition"] = (
            f'attachment; filename="drawing-{drawing.pk}.pdf"'
        )
        response["Cache-Control"] = "private, no-store"
        return response
