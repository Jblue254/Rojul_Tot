from rest_framework import serializers
from drawings.models import Drawing
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    drawing = serializers.PrimaryKeyRelatedField(
        queryset=Drawing.objects.all(),
        required=False
    )

    drawing_title = serializers.CharField(
        source='drawing.title',
        read_only=True
    )
    unit_price = serializers.DecimalField(
        source='drawing.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
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
            'drawing_title',
            'unit_price',
            'subtotal',
        ]

    def get_subtotal(self, obj):
        return obj.drawing.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'customer',
            'items',
            'total_amount',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'customer',
            'items',
            'total_amount',
            'created_at',
            'updated_at',
        ]

    def get_total_amount(self, obj):
        return sum(
            item.drawing.price * item.quantity
            for item in obj.items.select_related('drawing').all()
        )