from django.db import models
from datetime import date


# Create your models here.
class Employee(models.Model):
    name = models.CharField(
        max_length=30)

    email_address = models.EmailField()

    photo = models.URLField()

    birth_date = models.DateField()

    works_full_time = models.BooleanField()

    created_on = models.DateTimeField(auto_now_add=True)


class Department(models.Model):
    LOCATIONS = (
        ('Sofia', 'Sofia'),
        ('Plovdiv', 'Plovdiv'),
        ('Burgas', 'Burgas'),
        ('Varna', 'Varna')
    )
    code = models.CharField(
        max_length=4,
        primary_key=True,
        unique=True)

    name = models.CharField(
        max_length=50,
        unique=True)

    employees_count = models.PositiveIntegerField(
        verbose_name='Employees Count',
        default=1)

    location = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=LOCATIONS)

    last_edited_on = models.DateTimeField(
        auto_now=True,
        editable=False)

class Project(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
                   )

    description = models.TextField(
        null=True,
        blank=True
    )

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    duration_in_days = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Duration in Days'
    )

    estimated_hours = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Estimated Hours'
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Start Date',
        default=date.today
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    last_edited_on = models.DateTimeField(
        auto_now=True,
        editable=False
    )
