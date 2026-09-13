from django.urls import path
from .views import DashboardStatisticsView, UserStatisticsView, RentalOrderStatisticsView

urlpatterns = [
    path('dashboard/',DashboardStatisticsView.as_view(),name='dashboard-statistics'),
    path('users/',UserStatisticsView.as_view(),name='user-statistics'),
    path('rental-orders/',RentalOrderStatisticsView.as_view(),name='rental-order-statistics'),
]