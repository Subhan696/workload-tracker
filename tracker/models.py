from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees"
    )
    role = models.CharField(max_length=50, default="Engineer")
    pto_hours = models.FloatField(default=0.0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} - {self.department.code}"


class Assignment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        ON_HOLD = "ON_HOLD", "On Hold"

    title = models.CharField(max_length=150)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="assignments"
    )
    hours = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"[{self.status}] {self.title} ({self.hours}h) -> {self.employee.name}"
