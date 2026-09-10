from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from .models import Cart, CartItem
from .cart_serializers import CartSerializer, CartItemSerializer
from drawings.models import Drawing

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'ADMIN']:
            return Order.objects.all()

        return Order.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'ADMIN']:
            return Order.objects.all()

        return Order.objects.filter(customer=user)
    
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            customer=self.request.user
        )
        return cart


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(
            customer=self.request.user
        )

        drawing = serializer.validated_data['drawing']
        quantity = serializer.validated_data['quantity']

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            drawing=drawing
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

        from rest_framework.response import Response
        from rest_framework import status

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__customer=self.request.user
        )