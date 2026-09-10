from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(
        source='customer.email',
        read_only=True
    )

    manager_email = serializers.CharField(
        source='manager.email',
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'customer',
            'customer_email',
            'manager',
            'manager_email',
            'location',
            'budget',
            'start_date',
            'expected_end_date',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'customer',
            'customer_email',
            'manager_email',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        if data['expected_end_date'] <= data['start_date']:
            raise serializers.ValidationError({
                'expected_end_date': 'Expected end date must be after the start date.'
            })

        if data['budget'] < 0:
            raise serializers.ValidationError({
                'budget': 'Budget cannot be negative.'
            })

        return data