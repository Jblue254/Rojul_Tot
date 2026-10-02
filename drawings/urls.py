from django.urls import path

from .views import (
    DrawingCategoryListCreateView,
    DrawingCategoryDetailView,
    DrawingListCreateView,
    DrawingDetailView,
    PublicDrawingDetailView,
    PublicDrawingListView,
)

urlpatterns = [
    path(
        "categories/",
        DrawingCategoryListCreateView.as_view(),
        name="drawing-category-list-create",
    ),

    path(
        "categories/<int:pk>/",
        DrawingCategoryDetailView.as_view(),
        name="drawing-category-detail",
    ),

    path(
        "public/",
        PublicDrawingListView.as_view(),
        name="public-drawings",
    ),

    path(
        "",
        DrawingListCreateView.as_view(),
        name="drawing-list-create",
    ),

    path(
        "<int:pk>/",
        DrawingDetailView.as_view(),
        name="drawing-detail",
    ),
    path("public/<int:pk>/", PublicDrawingDetailView.as_view(), name="public-drawing-detail"),
]