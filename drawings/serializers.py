
from django.conf import settings
from rest_framework import serializers

from config.supabase_storage import upload_file, public_file_url
from .models import Drawing, DrawingCategory


class DrawingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawingCategory
        fields = "__all__"


class DrawingSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )
    preview_image = serializers.ImageField(
        required=False,
        allow_null=True,
        write_only=True,
    )
    drawing_file = serializers.FileField(
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Drawing
        fields = [
            "id", "title", "description", "category", "category_name",
            "price", "preview_image", "drawing_file", "status",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.preview_image:
            path = instance.preview_image.name
            if path.startswith(("http://", "https://")):
                data["preview_image"] = path
            elif getattr(settings, "SUPABASE_URL", ""):
                data["preview_image"] = public_file_url(
                    "drawing-previews", path
                )
            else:
                data["preview_image"] = None
        else:
            data["preview_image"] = None

        # Never expose a private PDF URL in a public or normal API response.
        data["drawing_file"] = None
        return data

    def create(self, validated_data):
        preview = validated_data.pop("preview_image", None)
        drawing_file = validated_data.pop("drawing_file", None)

        if preview:
            validated_data["preview_image"] = upload_file(
                preview, "drawing-previews", folder="previews"
            )

        if drawing_file:
            validated_data["drawing_file"] = upload_file(
                drawing_file, "drawing-files", folder="files"
            )

        return Drawing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        preview = validated_data.pop("preview_image", None)
        drawing_file = validated_data.pop("drawing_file", None)

        if preview:
            instance.preview_image = upload_file(
                preview, "drawing-previews", folder="previews"
            )

        if drawing_file:
            instance.drawing_file = upload_file(
                drawing_file, "drawing-files", folder="files"
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
