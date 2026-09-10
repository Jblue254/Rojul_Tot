from rest_framework import serializers
from .models import Category, Machine, Maintenance



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class MachineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Machine
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'description',
            'price_per_day',
            'quantity',
            'location',
            'status',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

class MaintenanceSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(
        source='machine.name',
        read_only=True
    )

    class Meta:
        model = Maintenance
        fields = [
            'id',
            'machine',
            'machine_name',
            'service_type',
            'description',
            'cost',
            'service_date',
            'next_service_date',
            'status',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'machine_name',
            'created_at',
        ]

    def validate(self, data):
        next_service_date = data.get('next_service_date')
        service_date = data.get('service_date')

        if (
            next_service_date and
            service_date and
            next_service_date <= service_date
        ):
            raise serializers.ValidationError({
                'next_service_date':
                'Next service date must be after service date.'
            })

        return data