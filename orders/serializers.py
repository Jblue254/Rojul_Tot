from rest_framework import serializers
from .models import Order, OrderItem
from drawings.models import Drawing


class OrderItemSerializer(serializers.ModelSerializer):
    drawing_title = serializers.CharField(
        source='drawing.title',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'drawing',
            'drawing_title',
            'quantity',
            'unit_price',
            'subtotal',
        ]
        read_only_fields = [
            'id',
            'unit_price',
            'subtotal',
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    customer_email = serializers.CharField(
        source='customer.email',
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'customer_email',
            'status',
            'total_amount',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'customer',
            'customer_email',
            'status',
            'total_amount',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        order = Order.objects.create(**validated_data)

        total_amount = 0

        for item_data in items_data:
            drawing = item_data['drawing']
            quantity = item_data['quantity']

            unit_price = drawing.price
            subtotal = unit_price * quantity

            OrderItem.objects.create(
                order=order,
                drawing=drawing,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )

            total_amount += subtotal

        order.total_amount = total_amount
        order.save()

        return order