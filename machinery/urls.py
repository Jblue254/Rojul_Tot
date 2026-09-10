from django.urls import path
from .views import (CategoryListCreateView,
    CategoryDetailView,
    MachineListCreateView,
    MachineDetailView,
    MaintenanceListCreateView,
    MaintenanceDetailView,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('machines/', MachineListCreateView.as_view(), name='machine-list-create'),
    path('machines/<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
    path('maintenances/', MaintenanceListCreateView.as_view(), name='maintenance-list-create'),
    path('maintenances/<int:pk>/', MaintenanceDetailView.as_view(), name='maintenance-detail'),
]