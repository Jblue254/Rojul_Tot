from rest_framework import serializers
from .models import Drawing


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = [
            'id',
            'title',
            'description',
            'category',
            'price',
            'preview_image',
            'drawing_file',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]