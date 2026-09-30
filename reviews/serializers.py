from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    machine_name = serializers.CharField(
        source="machine.name",
        read_only=True
    )

    drawing_title = serializers.CharField(
        source="drawing.title",
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "customer",
            "machine",
            "machine_name",
            "drawing",
            "drawing_title",
            "rating",
            "comment",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "customer",
            "created_at",
        ]

    def validate(self, data):
        machine = data.get("machine")
        drawing = data.get("drawing")

        if not machine and not drawing:
            raise serializers.ValidationError(
                "A review must be linked to either a machine or a drawing."
            )

        if machine and drawing:
            raise serializers.ValidationError(
                "A review cannot be linked to both a machine and a drawing."
            )

        return data