from django.contrib import admin
from .models import (
    Project,
    ProjectMachine,
    ProjectMember
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "customer",
        "manager",
        "status",
        "budget",
        "start_date",
        "expected_end_date",
    )

    search_fields = (
        "name",
        "location",
    )

    list_filter = (
        "status",
        "start_date",
    )


@admin.register(ProjectMachine)
class ProjectMachineAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "machine",
        "quantity",
        "assigned_at",
    )

    search_fields = (
        "project__name",
        "machine__name",
    )


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "project",
        "role",
        "phone",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "project__name",
    )

    list_filter = (
        "role",
    )