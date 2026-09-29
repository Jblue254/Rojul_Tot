from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectDetailView,
    ProjectMachineListCreateView,
    ProjectMachineDetailView,
    ProjectMemberDetailView,
    ProjectMemberListCreateView,
)


urlpatterns = [
    path(
        '',
        ProjectListCreateView.as_view(),
        name='project-list-create'
    ),

    path(
        '<int:pk>/',
        ProjectDetailView.as_view(),
        name='project-detail'
    ),

    path(
        'machines/',
        ProjectMachineListCreateView.as_view(),
        name='project-machine-list-create'
    ),

    path(
        'machines/<int:pk>/',
        ProjectMachineDetailView.as_view(),
        name='project-machine-detail'
    ),
    path(
    'members/',
    ProjectMemberListCreateView.as_view(),
    name='project-member-list-create'
),

path(
    'members/<int:pk>/',
    ProjectMemberDetailView.as_view(),
    name='project-member-detail'
),

]