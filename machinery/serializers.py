from rest_framework import serializers
from .models import Category, Machine


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