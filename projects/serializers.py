from rest_framework import serializers
from .models import (
    Project,
    ProjectMachine,
    ProjectMember,
    ProjectExpense,
    ProjectMilestone,
    Review,
)


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
    'image',
    'featured',
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

class ReviewSerializer(
    serializers.ModelSerializer
):

    project_name = serializers.CharField(
        source="project.name",
        read_only=True
    )

    class Meta:
        model = Review
        fields = "__all__"