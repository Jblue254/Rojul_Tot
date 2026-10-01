from django.urls import path

from .views import (
    FeaturedProjectListView,
    PublicProjectListView,
    ProjectListCreateView,
    ProjectDetailView,
    ProjectMachineListCreateView,
    ProjectMachineDetailView,
    ProjectMemberListCreateView,
    ProjectMemberDetailView,
    ProjectExpenseListCreateView,
    ProjectExpenseDetailView,
    ProjectMilestoneListCreateView,
    ProjectMilestoneDetailView,
    ReviewListCreateView,
    ReviewDetailView,
)

urlpatterns = [
    # Public endpoints
    path(
        "public/",
        PublicProjectListView.as_view(),
        name="public-projects",
    ),

    path(
        "featured/",
        FeaturedProjectListView.as_view(),
        name="featured-projects",
    ),

    # Projects
    path(
        "",
        ProjectListCreateView.as_view(),
        name="project-list-create",
    ),

    path(
        "<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),

    # Machines
    path(
        "machines/",
        ProjectMachineListCreateView.as_view(),
        name="project-machine-list-create",
    ),

    path(
        "machines/<int:pk>/",
        ProjectMachineDetailView.as_view(),
        name="project-machine-detail",
    ),

    # Members
    path(
        "members/",
        ProjectMemberListCreateView.as_view(),
        name="project-member-list-create",
    ),

    path(
        "members/<int:pk>/",
        ProjectMemberDetailView.as_view(),
        name="project-member-detail",
    ),

    # Expenses
    path(
        "expenses/",
        ProjectExpenseListCreateView.as_view(),
        name="project-expense-list-create",
    ),

    path(
        "expenses/<int:pk>/",
        ProjectExpenseDetailView.as_view(),
        name="project-expense-detail",
    ),

    # Milestones
    path(
        "milestones/",
        ProjectMilestoneListCreateView.as_view(),
        name="project-milestone-list-create",
    ),

    path(
        "milestones/<int:pk>/",
        ProjectMilestoneDetailView.as_view(),
        name="project-milestone-detail",
    ),

    # Reviews
    path(
        "reviews/",
        ReviewListCreateView.as_view(),
        name="review-list-create",
    ),

    path(
        "reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="review-detail",
    ),
]