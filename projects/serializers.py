from rest_framework import serializers
from .models import (
    Project,
    ProjectMachine,
    ProjectMember,
    ProjectExpense,
    ProjectMilestone,
    Review,
)



from django.conf import settings
from rest_framework import serializers

from config.supabase_storage import upload_file, public_file_url
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(
        source="customer.email",
        read_only=True,
    )
    manager_email = serializers.CharField(
        source="manager.email",
        read_only=True,
    )
    image = serializers.ImageField(
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Project
        fields = [
            "id", "name", "description", "image", "featured",
            "customer", "customer_email", "manager", "manager_email",
            "location", "budget", "start_date", "expected_end_date",
            "status", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "customer", "customer_email", "manager_email",
            "created_at", "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not instance.image:
            data["image"] = None
            return data

        path = instance.image.name

        if path.startswith(("http://", "https://")):
            data["image"] = path
        elif getattr(settings, "SUPABASE_URL", ""):
            data["image"] = public_file_url("project-images", path)
        else:
            data["image"] = None

        return data

    def create(self, validated_data):
        image = validated_data.pop("image", None)

        if image:
            validated_data["image"] = upload_file(
                image,
                "project-images",
                folder="projects",
            )

        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)

        if image:
            instance.image = upload_file(
                image,
                "project-images",
                folder="projects",
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate(self, data):
        start_date = data.get(
            "start_date",
            getattr(self.instance, "start_date", None),
        )
        end_date = data.get(
            "expected_end_date",
            getattr(self.instance, "expected_end_date", None),
        )
        budget = data.get(
            "budget",
            getattr(self.instance, "budget", None),
        )

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                "expected_end_date":
                    "Expected end date must be after the start date."
            })

        if budget is not None and budget < 0:
            raise serializers.ValidationError({
                "budget": "Budget cannot be negative."
            })

        return data


class ProjectMemberSerializer(
    serializers.ModelSerializer
):
    project_name = serializers.CharField(
        source='project.name',
        read_only=True
    )

    class Meta:
        model = ProjectMember
        fields = '__all__'

class ProjectMachineSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(
        source='machine.name',
        read_only=True
    )

    project_name = serializers.CharField(
        source='project.name',
        read_only=True
    )

    class Meta:
        model = ProjectMachine
        fields = '__all__'

class ProjectExpenseSerializer(
    serializers.ModelSerializer
):
    project_name = serializers.CharField(
        source='project.name',
        read_only=True
    )

    created_by_email = serializers.CharField(
        source='created_by.email',
        read_only=True
    )

    class Meta:
        model = ProjectExpense
        fields = '__all__'

class ProjectMilestoneSerializer(
    serializers.ModelSerializer
):
    project_name = serializers.CharField(
        source='project.name',
        read_only=True
    )

    class Meta:
        model = ProjectMilestone
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "customer",
            "customer_name",
            "project",
            "project_name",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "customer",
            "customer_name",
            "created_at",
        ]

    def get_customer_name(self, obj):
        customer = obj.customer

        full_name = (
            f"{customer.first_name} {customer.last_name}"
        ).strip()

        if full_name:
            return full_name

        return (
            getattr(customer, "username", None)
            or getattr(customer, "email", None)
            or f"Customer #{customer.pk}"
        )