
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Payment(models.Model):
    class Status(models.TextChoices):
        INITIATED = "INITIATED", "Initiated"
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Successful"
        FAILED = "FAILED", "Failed"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    # A payment must belong to an order OR a rental, never both.
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="payments",
    )
    rental = models.ForeignKey(
        "rentals.Rental",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    phone_number = models.CharField(max_length=12)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INITIATED,
    )

    merchant_request_id = models.CharField(
        max_length=100,
        blank=True,
    )
    checkout_request_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    mpesa_receipt_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    result_code = models.CharField(max_length=20, blank=True)
    result_description = models.TextField(blank=True)
    callback_payload = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if bool(self.order_id) == bool(self.rental_id):
            raise ValidationError(
                "A payment must belong to exactly one order or rental."
            )

        if self.order_id and self.customer_id:
            if self.order.customer_id != self.customer_id:
                raise ValidationError(
                    "The payment customer must own the order."
                )

        if self.rental_id and self.customer_id:
            if self.rental.customer_id != self.customer_id:
                raise ValidationError(
                    "The payment customer must own the rental."
                )

    def __str__(self):
        return f"Payment #{self.pk} - {self.status}"
