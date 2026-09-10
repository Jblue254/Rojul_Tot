from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Machine(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        RENTED = 'RENTED', 'Rented'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'
        UNAVAILABLE = 'UNAVAILABLE', 'Unavailable'

    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='machines'
    )
    description = models.TextField()
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )
    image = models.ImageField(
        upload_to='machinery/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Maintenance(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )

    service_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    service_date = models.DateField()

    next_service_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.machine.name} - {self.service_type}"