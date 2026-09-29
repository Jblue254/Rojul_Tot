from rest_framework import generics
from accounts.permissions import IsManagerOrAdmin
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ProjectExpenseSerializer,
    ProjectMemberSerializer,
    ProjectMilestoneSerializer,
    ProjectSerializer,
    ProjectMachineSerializer,
)
from .models import (
    Project,
    ProjectMachine,
    ProjectMember,
    ProjectExpense,
    ProjectMilestone,
)

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'ADMIN']:
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.filter(customer=user)

        search = self.request.query_params.get('search')
        status = self.request.query_params.get('status')
        location = self.request.query_params.get('location')
        min_budget = self.request.query_params.get('min_budget')
        max_budget = self.request.query_params.get('max_budget')

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        if min_budget:
            queryset = queryset.filter(
                budget__gte=min_budget
            )

        if max_budget:
            queryset = queryset.filter(
                budget__lte=max_budget
            )

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'ADMIN']:
            return Project.objects.all()

        return Project.objects.filter(customer=user)

class ProjectMachineListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = ProjectMachineSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMachine.objects.select_related(
            'project',
            'machine'
        )

class ProjectMachineDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ProjectMachineSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMachine.objects.select_related(
            'project',
            'machine'
        )

class ProjectMemberListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMember.objects.select_related(
            'project'
        )
class ProjectMemberDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMember.objects.select_related(
            'project'
        )

class ProjectExpenseListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = ProjectExpenseSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectExpense.objects.select_related(
            'project',
            'created_by'
        )

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user
        )


class ProjectExpenseDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ProjectExpenseSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectExpense.objects.select_related(
            'project',
            'created_by'
        )

class ProjectMilestoneListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = ProjectMilestoneSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMilestone.objects.select_related(
            'project'
        )


class ProjectMilestoneDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ProjectMilestoneSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMilestone.objects.select_related(
            'project'
        )