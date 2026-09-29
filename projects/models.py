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
class ProjectMember(models.Model):

    ROLE_CHOICES = [
    ('FOREMAN', 'Foreman'),
    ('WORKER', 'Worker'),
    ('ELECTRICIAN', 'Electrician'),
    ('PLUMBER', 'Plumber'),
    ('MASON', 'Mason'),
    ('CARPENTER', 'Carpenter'),
    ('PAINTER', 'Painter'),
    ('WELDER', 'Welder'),
]



    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )

    full_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    role = models.CharField(
    max_length=20,
    choices=ROLE_CHOICES,
    default='WORKER'
)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class ProjectMachine(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='assigned_machines'
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

    def clean(self):
        super().clean()
        if self.machine and self.quantity > self.machine.quantity:
            raise ValidationError({
                'quantity': f'Only {self.machine.quantity} machine(s) available.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'machine'],
                name='unique_project_machine'
            )
        ]

    def __str__(self):
        return f"{self.project.name} - {self.machine.name} ({self.quantity})"

class ProjectExpense(models.Model):

    CATEGORY_CHOICES = [
        ('MATERIALS', 'Materials'),
        ('LABOUR', 'Labour'),
        ('MACHINERY', 'Machinery'),
        ('TRANSPORT', 'Transport'),
        ('FUEL', 'Fuel'),
        ('OTHER', 'Other'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    title = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.project.name} - {self.title}"