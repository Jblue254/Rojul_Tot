from django.urls import path
from .views import RentalListCreateView, RentalDetailView

urlpatterns = [
    path('', RentalListCreateView.as_view(), name='rental-list-create'),
    path('<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
]