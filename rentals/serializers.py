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

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date.'
            })

        if data['quantity'] <= 0:
            raise serializers.ValidationError({
                'quantity': 'Quantity must be greater than zero.'
            })

        if data['quantity'] > data['machine'].quantity:
            raise serializers.ValidationError({
                'quantity': 'Requested quantity is not available.'
            })

        return data

    def create(self, validated_data):
        machine = validated_data['machine']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        quantity = validated_data['quantity']

        rental_days = (end_date - start_date).days

        total_price = (
            machine.price_per_day
            * quantity
            * rental_days
        )

        validated_data['total_price'] = total_price

        return Rental.objects.create(**validated_data)