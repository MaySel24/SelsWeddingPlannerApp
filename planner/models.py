from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from typing import Any

# Guest List Model
class Guest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    rsvp_status = models.CharField(
        max_length=8,
        choices=[('Yes', 'Yes'), ('No', 'No'), ('Pending', 'Pending')],
        default='Pending'
    )
    table_number = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['created_at']  # Orders guests by creation date

    def __str__(self):
        return self.name

# Task Model
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255, verbose_name="Task Title")
    description = models.TextField(null=True, blank=True, verbose_name="Task Description")
    due_date = models.DateField(null=True, blank=True, verbose_name="Due Date")
    assigned_to = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Assigned To"
    )  # Changed from ForeignKey to CharField
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        ordering = ['-due_date', 'status']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# Vendor Model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contract_signed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)  # New field

    def __str__(self):
        return self.name

# Budget Model
class Budget(models.Model):
    category = models.CharField(max_length=255)
    amount_allocated = models.DecimalField(max_digits=10, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def remaining_balance(self):
        return self.amount_allocated - self.amount_spent

    def __str__(self):
        return f"{self.category}: {self.amount_allocated}"

# Total Budget
class TotalBudget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)  # Track last update

    def _str_(self):
        return f"Total Budget: {self.amount}"

# Wedding Colors
class WeddingColor(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Blush Pink"
    hex_code = models.CharField(max_length=7, help_text="Enter a HEX code like #FFC0CB")  # Store HEX values

    def __str__(self):
        return self.name

# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"