
from django.conf import settings
from rest_framework import serializers

from config.supabase_storage import upload_file, public_file_url
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone",
            "password",
            "password_confirm",
        ]

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
    )
    profile_image = serializers.ImageField(
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "password",
            "role",
            "profile_image",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not instance.profile_image:
            data["profile_image"] = None
            return data

        path = instance.profile_image.name

        if path.startswith(("http://", "https://")):
            data["profile_image"] = path
        elif getattr(settings, "SUPABASE_URL", ""):
            data["profile_image"] = public_file_url(
                "profile-images",
                path,
            )
        else:
            data["profile_image"] = None

        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        image = validated_data.pop("profile_image", None)

        user = User(**validated_data)

        if password:
            user.set_password(password)

        if image:
            user.profile_image = upload_file(
                image,
                "profile-images",
                folder="profiles",
            )

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        image = validated_data.pop("profile_image", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        if image:
            instance.profile_image = upload_file(
                image,
                "profile-images",
                folder="profiles",
            )

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
