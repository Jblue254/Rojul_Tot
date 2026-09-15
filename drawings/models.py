from django.db import models


class DrawingCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Drawing(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        SOLD_OUT = 'SOLD_OUT', 'Sold Out'
        INACTIVE = 'INACTIVE', 'Inactive'

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.ForeignKey(
        DrawingCategory,
        on_delete=models.CASCADE,
        related_name='drawings',
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    preview_image = models.ImageField(
        upload_to='drawings/previews/',
        blank=True,
        null=True
    )

    drawing_file = models.FileField(
        upload_to='drawings/files/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title