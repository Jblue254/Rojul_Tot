from django.urls import path
from .views import DashboardStatisticsView, UserStatisticsView

urlpatterns = [
    path('dashboard/',DashboardStatisticsView.as_view(),name='dashboard-statistics'),
    path('users/',UserStatisticsView.as_view(),name='user-statistics'),
]