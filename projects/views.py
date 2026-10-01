from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.permissions import IsManagerOrAdmin
from notifications.models import Notification
from notifications.utils import create_notification

from .models import (
    Project,
    ProjectExpense,
    ProjectMachine,
    ProjectMember,
    ProjectMilestone,
    Review,
)
from .serializers import (
    ProjectExpenseSerializer,
    ProjectMachineSerializer,
    ProjectMemberSerializer,
    ProjectMilestoneSerializer,
    ProjectSerializer,
    ReviewSerializer,
)


class PublicProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Project.objects.filter(
            status=Project.Status.COMPLETED
        ).order_by("-created_at")


class FeaturedProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Project.objects.filter(
            featured=True,
            status=Project.Status.COMPLETED
        ).order_by("-created_at")


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ["MANAGER", "ADMIN"]:
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.filter(customer=user)

        search = self.request.query_params.get("search")
        status = self.request.query_params.get("status")
        location = self.request.query_params.get("location")
        min_budget = self.request.query_params.get("min_budget")
        max_budget = self.request.query_params.get("max_budget")

        if search:
            queryset = queryset.filter(name__icontains=search)
        if status:
            queryset = queryset.filter(status=status)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_budget:
            queryset = queryset.filter(budget__gte=min_budget)
        if max_budget:
            queryset = queryset.filter(budget__lte=max_budget)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        project = serializer.save(customer=self.request.user)

        create_notification(
            recipient=project.customer,
            title="Project Created",
            message=f"Project '{project.name}' has been created successfully.",
            notification_type=Notification.NotificationType.PROJECT,
        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ["MANAGER", "ADMIN"]:
            return Project.objects.all()

        return Project.objects.filter(customer=user)

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        project = serializer.save()

        if old_status != project.status and project.status == "COMPLETED":
            create_notification(
                recipient=project.customer,
                title="Project Completed",
                message=f"Project '{project.name}' has been completed.",
                notification_type=Notification.NotificationType.PROJECT,
            )


class ProjectMachineListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectMachineSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMachine.objects.select_related("project", "machine")


class ProjectMachineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectMachineSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMachine.objects.select_related("project", "machine")


class ProjectMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMember.objects.select_related("project")

    def perform_create(self, serializer):
        serializer.save()


class ProjectMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMember.objects.select_related("project")

    def perform_destroy(self, instance):
        instance.delete()


class ProjectExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectExpenseSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectExpense.objects.select_related("project", "created_by")

    def perform_create(self, serializer):
        expense = serializer.save(created_by=self.request.user)

        create_notification(
            recipient=expense.project.customer,
            title="Project Expense Added",
            message=f"An expense of KES {expense.amount} was added to project '{expense.project.name}'.",
            notification_type=Notification.NotificationType.PROJECT,
        )


class ProjectExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectExpenseSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectExpense.objects.select_related("project", "created_by")


class ProjectMilestoneListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectMilestoneSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMilestone.objects.select_related("project")

    def perform_create(self, serializer):
        milestone = serializer.save()

        create_notification(
            recipient=milestone.project.customer,
            title="New Project Milestone",
            message=f"Milestone '{milestone.title}' was added to project '{milestone.project.name}'.",
            notification_type=Notification.NotificationType.PROJECT,
        )


class ProjectMilestoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectMilestoneSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        return ProjectMilestone.objects.select_related("project")

    def perform_update(self, serializer):
        old_completed = serializer.instance.completed
        milestone = serializer.save()

        if not old_completed and milestone.completed:
            create_notification(
                recipient=milestone.project.customer,
                title="Milestone Completed",
                message=f"Milestone '{milestone.title}' has been completed.",
                notification_type=Notification.NotificationType.PROJECT,
            )


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.select_related("project", "customer")

    def perform_create(self, serializer):
        review = serializer.save(customer=self.request.user)

        create_notification(
            recipient=review.project.customer,
            title="New Review",
            message=f"You received a {review.rating}/5 review for project '{review.project.name}'.",
            notification_type=Notification.NotificationType.PROJECT,
        )


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.select_related("project", "customer")