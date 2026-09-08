from django.contrib import admin
from .models import Category, Machine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price_per_day',
        'quantity',
        'status',
        'location',
    )
    list_filter = ('status', 'category')
    search_fields = ('name', 'location')