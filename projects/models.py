from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from machinery.models import Machine


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'Planning'
        ACTIVE = 'ACTIVE', 'Active'
        ON_HOLD = 'ON_HOLD', 'On Hold'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects'
    )

    location = models.CharField(max_length=255)

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    start_date = models.DateField()
    expected_end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.start_date and self.expected_end_date and self.expected_end_date < self.start_date:
            raise ValidationError({
                'expected_end_date': 'Expected end date cannot be earlier than the start date.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ProjectMachine(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='machine_assignments'
    )

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name='project_assignments'
    )

    quantity = models.PositiveIntegerField(default=1)

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'machine'],
                name='unique_project_machine'
            )
        ]

    def __str__(self):
        return f"{self.project.name} - {self.machine.name} ({self.quantity})"