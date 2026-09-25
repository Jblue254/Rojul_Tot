from django.urls import path
from .views import (
    RentalListCreateView,
    RentalDetailView,
    ApproveRentalView,
    RejectRentalView,
    ActivateRentalView,
    CompleteRentalView,
)

urlpatterns = [
    path(
        '',
        RentalListCreateView.as_view(),
        name='rental-list-create'
    ),

    path(
        '<int:pk>/',
        RentalDetailView.as_view(),
        name='rental-detail'
    ),

    path(
        '<int:pk>/approve/',
        ApproveRentalView.as_view(),
        name='rental-approve'
    ),

    path(
        '<int:pk>/reject/',
        RejectRentalView.as_view(),
        name='rental-reject'
    ),

    path(
        '<int:pk>/complete/',
        CompleteRentalView.as_view(),
        name='rental-complete'
    ),
    path(
    '<int:pk>/activate/',
    ActivateRentalView.as_view(),
    name='rental-activate'
),
]