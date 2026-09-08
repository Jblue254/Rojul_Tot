from rest_framework import serializers
from .models import Rental


class RentalSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(
        source='customer.email',
        read_only=True
    )

    machine_name = serializers.CharField(
        source='machine.name',
        read_only=True
    )

    class Meta:
        model = Rental
        fields = [
            'id',
            'customer',
            'customer_email',
            'machine',
            'machine_name',
            'start_date',
            'end_date',
            'quantity',
            'total_price',
            'status',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'customer',
            'total_price',
            'status',
            'created_at',
            'updated_at',
        ]