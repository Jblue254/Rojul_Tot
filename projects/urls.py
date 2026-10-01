from django.urls import path
from .views import (
    FeaturedProjectListView,
    ProjectExpenseDetailView,
    ProjectExpenseListCreateView,
    ProjectListCreateView,
    ProjectDetailView,
    ProjectMachineListCreateView,
    ProjectMachineDetailView,
    ProjectMemberDetailView,
    ProjectMemberListCreateView,
    ProjectMilestoneDetailView,
    ProjectMilestoneListCreateView,
    PublicProjectListView,
    ReviewDetailView,
    ReviewListCreateView,
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
path(
    'expenses/',
    ProjectExpenseListCreateView.as_view(),
    name='project-expense-list-create'
),

path(
    'expenses/<int:pk>/',
    ProjectExpenseDetailView.as_view(),
    name='project-expense-detail'
),
path(
    'milestones/',
    ProjectMilestoneListCreateView.as_view(),
    name='project-milestone-list-create'
),

path(
    'milestones/<int:pk>/',
    ProjectMilestoneDetailView.as_view(),
    name='project-milestone-detail'
),
path(
    "reviews/",
    ReviewListCreateView.as_view()
),

path(
    "reviews/<int:pk>/",
    ReviewDetailView.as_view()
),
path(
    "public/",
        PublicProjectListView.as_view(),
    name="public-projects"
),

path(
    "featured/",
        FeaturedProjectListView.as_view(),
    name="featured-projects"
),

]