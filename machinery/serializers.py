
from pathlib import Path

from django.conf import settings
from rest_framework import serializers

from config.supabase_storage import upload_file, public_file_url
from .models import Category, Machine, Maintenance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class MachineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )
    image = serializers.ImageField(
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Machine
        fields = [
            "id", "name", "category", "category_name", "description",
            "price_per_day", "quantity", "location", "status",
            "image", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not instance.image:
            data["image"] = None
            return data

        path = instance.image.name
        base_url = getattr(settings, "SUPABASE_URL", "").rstrip("/")

        if not base_url:
            data["image"] = None
            return data

        # New uploads are stored using their full object path.
        # Existing files uploaded to the bucket root are also supported.
        if path.startswith("http://") or path.startswith("https://"):
            data["image"] = path
        else:
            data["image"] = public_file_url(
                "machinery-images",
                path,
            )

        return data

    def create(self, validated_data):
        image = validated_data.pop("image", None)

        if image:
            path = upload_file(
                image,
                "machinery-images",
                folder="machinery",
            )
            validated_data["image"] = path

        return Machine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)

        if image:
            path = upload_file(
                image,
                "machinery-images",
                folder="machinery",
            )
            instance.image = path

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MaintenanceSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(
        source="machine.name",
        read_only=True,
    )

    class Meta:
        model = Maintenance
        fields = [
            "id", "machine", "machine_name", "service_type",
            "description", "cost", "service_date",
            "next_service_date", "status", "created_at",
        ]
        read_only_fields = ["id", "machine_name", "created_at"]

    def validate(self, data):
        next_service_date = data.get("next_service_date")
        service_date = data.get("service_date")

        if (
            next_service_date
            and service_date
            and next_service_date <= service_date
        ):
            raise serializers.ValidationError({
                "next_service_date":
                    "Next service date must be after service date."
            })

        return data
