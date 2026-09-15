from django.urls import path

from .views import DrawingCategoryListCreateView,DrawingCategoryDetailView,DrawingListCreateView,DrawingDetailView



urlpatterns = [
    path('categories/',DrawingCategoryListCreateView.as_view(),name='drawing-category-list-create'),
    path('categories/<int:pk>/',DrawingCategoryDetailView.as_view(),name='drawing-category-detail'),
    path('',DrawingListCreateView.as_view(),name='drawing-list-create'),
    path('<int:pk>/',DrawingDetailView.as_view(),name='drawing-detail'),
]