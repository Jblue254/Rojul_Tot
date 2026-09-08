from django.contrib import admin
from .models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'machine',
        'start_date',
        'end_date',
        'quantity',
        'total_price',
        'status',
    )

    list_filter = ('status', 'start_date', 'end_date')
    search_fields = (
        'customer__email',
        'machine__name',
    )