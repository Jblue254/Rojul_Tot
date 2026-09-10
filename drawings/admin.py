from django.contrib import admin
from .models import Drawing


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'price',
        'status',
        'created_at',
    )

    list_filter = (
        'category',
        'status',
    )

    search_fields = (
        'title',
        'category',
    )