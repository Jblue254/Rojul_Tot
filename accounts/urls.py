from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
    AdminOnlyView,
    AdminUserListCreateView,
    AdminUserDetailView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),

    path('admin-only/', AdminOnlyView.as_view()),

    path(
        'users/',
        AdminUserListCreateView.as_view(),
        name='admin-user-list'
    ),

    path(
        'users/<int:pk>/',
        AdminUserDetailView.as_view(),
        name='admin-user-detail'
    ),
]