from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Category, Machine, Maintenance
from .serializers import CategorySerializer, MachineSerializer, MaintenanceSerializer
from accounts.permissions import IsEquipmentManagerOrAdmin


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MachineListCreateView(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MachineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MaintenanceListCreateView(generics.ListCreateAPIView):
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated, IsEquipmentManagerOrAdmin]

    def get_queryset(self):
        return Maintenance.objects.all()


class MaintenanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated, IsEquipmentManagerOrAdmin]

    def get_queryset(self):
        return Maintenance.objects.all()