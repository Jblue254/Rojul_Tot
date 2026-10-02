from django.urls import path

from .views import (
    ContactMessageCreateView,
    ContactMessageListView,
    ContactMessageDetailView,
)

urlpatterns = [
    path(
        "public/",
        ContactMessageCreateView.as_view(),
        name="contact-create",
    ),

    path(
        "",
        ContactMessageListView.as_view(),
        name="contact-list",
    ),

    path(
        "<int:pk>/",
        ContactMessageDetailView.as_view(),
        name="contact-detail",
    ),
]