from django.db import models
from django.conf import settings
from machinery.models import Machine
from drawings.models import Drawing


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    drawing = models.ForeignKey(
        Drawing,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.email} - {self.rating}"