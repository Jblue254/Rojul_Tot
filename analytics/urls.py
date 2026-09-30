from django.urls import path
from .views import DashboardStatisticsView,ManagerDashboardView, UserStatisticsView, RentalOrderStatisticsView, ProjectStatisticsView,  AdminDashboardView
from .views import EquipmentManagerDashboardView
urlpatterns = [
    path('dashboard/',DashboardStatisticsView.as_view(),name='dashboard-statistics'),
    path('users/',UserStatisticsView.as_view(),name='user-statistics'),
    path('rental-orders/',RentalOrderStatisticsView.as_view(),name='rental-order-statistics'),
    path('projects/',ProjectStatisticsView.as_view(),name='project-statistics'),
    path('admin-dashboard/',AdminDashboardView.as_view(),name='admin-dashboard'),
    path('manager-dashboard/',ManagerDashboardView.as_view(),name="manager-dashboard"),
    path("equipment-dashboard/", EquipmentManagerDashboardView.as_view(),name="equipment-dashboard",
),

]       
