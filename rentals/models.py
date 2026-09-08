from django.db import models
from django.conf import settings
from machinery.models import Machine


class Rental(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rentals'
    )
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name='rentals'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.email} - {self.machine.name}"