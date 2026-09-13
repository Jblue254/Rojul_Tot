from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['MANAGER', 'ADMIN']:
            return Project.objects.all()

        return Project.objects.filter(customer=user)

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

def get_queryset(self):
    queryset = Project.objects.all()

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

    return queryset