from django.urls import path
from .views import DrawingListCreateView, DrawingDetailView


urlpatterns = [
    path('', DrawingListCreateView.as_view(), name='drawing-list-create'),
    path('<int:pk>/', DrawingDetailView.as_view(), name='drawing-detail'),
]