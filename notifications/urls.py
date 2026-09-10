from django.urls import path
from .views import (NotificationListView,NotificationDetailView,NotificationCreateView,)


urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('create/', NotificationCreateView.as_view(), name='notification-create'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]