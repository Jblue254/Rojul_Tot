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

def get_queryset(self):
    queryset = Machine.objects.all()

    search = self.request.query_params.get('search')
    category = self.request.query_params.get('category')
    status = self.request.query_params.get('status')
    location = self.request.query_params.get('location')
    min_price = self.request.query_params.get('min_price')
    max_price = self.request.query_params.get('max_price')

    if search:
        queryset = queryset.filter(
            name__icontains=search
        )

    if category:
        queryset = queryset.filter(
            category_id=category
        )

    if status:
        queryset = queryset.filter(
            status=status
        )

    if location:
        queryset = queryset.filter(
            location__icontains=location
        )

    if min_price:
        queryset = queryset.filter(
            price_per_day__gte=min_price
        )

    if max_price:
        queryset = queryset.filter(
            price_per_day__lte=max_price
        )

    return queryset

def get_queryset(self):
    queryset = Maintenance.objects.all()

    machine = self.request.query_params.get('machine')
    status = self.request.query_params.get('status')
    service_type = self.request.query_params.get('service_type')
    service_date = self.request.query_params.get('service_date')

    if machine:
        queryset = queryset.filter(
            machine_id=machine
        )

    if status:
        queryset = queryset.filter(
            status=status
        )

    if service_type:
        queryset = queryset.filter(
            service_type__icontains=service_type
        )

    if service_date:
        queryset = queryset.filter(
            service_date=service_date
        )

    return queryset