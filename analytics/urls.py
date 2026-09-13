from django.urls import path
from .views import DashboardStatisticsView

urlpatterns = [
    path('dashboard/',DashboardStatisticsView.as_view(),name='dashboard-statistics'),
]