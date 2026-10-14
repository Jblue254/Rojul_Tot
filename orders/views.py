import os

from django.db import transaction
from django.http import HttpResponse

from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.supabase_storage import download_private_file
from drawings.models import Drawing

from .cart_serializers import CartItemSerializer, CartSerializer
from .models import Cart, CartItem, Order, OrderItem
from .serializers import OrderSerializer
from notifications.utils import create_notification
from notifications.models import Notification


class DrawingDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        # Find the order item belonging to the logged-in customer.
        item = OrderItem.objects.select_related(
            "order", "drawing"
        ).filter(
            pk=item_id,
            order__customer=request.user,
        ).first()

        if item is None:
            raise NotFound(
                f"Order item {item_id} was not found for your account."
            )

        if item.order.status not in [
            "PAID",
            "PROCESSING",
            "COMPLETED",
        ]:
            raise PermissionDenied(
                "Your order must be paid before downloading this drawing."
            )

        drawing = item.drawing

        if not drawing or not drawing.drawing_file:
            raise NotFound(
                "This order item has no associated drawing file."
            )

        try:
            file_path = drawing.drawing_file.name
            content = download_private_file("drawing-files", file_path)

            if not content:
                raise NotFound("The drawing file is empty or unavailable.")
        except NotFound:
            raise
        except Exception:
            return Response(
                {"detail": "Unable to retrieve the drawing file from storage."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        filename = os.path.basename(file_path) or f"drawing-{drawing.pk}.pdf"

        response = HttpResponse(
            content,
            content_type="application/pdf",
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{filename}"'
        )
        response["Cache-Control"] = "private, no-store"
        return response


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['MANAGER', 'ADMIN', 'ARCHITECTURAL_MANAGER']:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(customer=user)

        # Filtering by query parameters
        status_param = self.request.query_params.get('status')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if min_amount:
            queryset = queryset.filter(total_amount__gte=min_amount)

        if max_amount:
            queryset = queryset.filter(total_amount__lte=max_amount)

        return queryset

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'ADMIN', 'ARCHITECTURAL_MANAGER']:
            return Order.objects.all()

        return Order.objects.filter(customer=user)

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        order = serializer.save()

        if old_status != order.status:
            first_item = order.items.first()
            order_name = (
                first_item.drawing.title
                if first_item
                else f"Order #{order.id}"
            )

            create_notification(
                recipient=order.customer,
                title="Order Status Updated",
                message=(
                    f"Your order for '{order_name}' "
                    f"has been updated to {order.status}."
                ),
                notification_type=Notification.NotificationType.ORDER
            )


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(customer=self.request.user)
        return cart


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(customer=self.request.user)

        drawing = serializer.validated_data['drawing']
        quantity = serializer.validated_data['quantity']

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, drawing=drawing
        )

        if item_created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

        # Store the actual CartItem instance for the response
        self.created_cart_item = cart_item

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = self.get_serializer(self.created_cart_item)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer=self.request.user)


class CartCheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Wrap checkout in an atomic transaction to ensure data integrity
        with transaction.atomic():
            cart, created = Cart.objects.get_or_create(customer=request.user)

            cart_items = cart.items.select_related('drawing').all()

            if not cart_items.exists():
                return Response(
                    {'detail': 'Your cart is empty.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            order = Order.objects.create(customer=request.user)

            total_amount = 0

            for cart_item in cart_items:
                drawing = cart_item.drawing
                quantity = cart_item.quantity

                unit_price = drawing.price
                subtotal = unit_price * quantity

                OrderItem.objects.create(
                    order=order,
                    drawing=drawing,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal,
                )

                total_amount += subtotal

            order.total_amount = total_amount
            order.save()
            
            create_notification(
                recipient=request.user,
                title="Order Created",
                message=f"Order #{order.id} has been placed successfully.",
                notification_type=Notification.NotificationType.ORDER
            )

            # Clear the cart after a successful checkout
            cart.items.all().delete()

            serializer = self.get_serializer(order)

            return Response(serializer.data, status=status.HTTP_201_CREATED)