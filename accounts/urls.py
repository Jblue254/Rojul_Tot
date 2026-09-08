from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    AdminOnlyView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('admin-only/', AdminOnlyView.as_view()),
]

