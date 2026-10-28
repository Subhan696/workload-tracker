"""Django Admin configuration for Workload Tracker models."""

from django.contrib import admin

from .models import Assignment, Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "department", "role", "pto_hours")
    list_filter = ("department", "role")
    search_fields = ("name", "email")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "employee", "hours", "status")
    list_filter = ("status", "employee__department")
    search_fields = ("title", "employee__name")
