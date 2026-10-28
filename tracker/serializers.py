"""DRF Serializers for Workload Tracker models."""

from rest_framework import serializers

from .models import Assignment, Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""

    class Meta:
        model = Department
        fields = ["id", "name", "code"]


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model."""

    department_name = serializers.ReadOnlyField(source="department.name")
    department_code = serializers.ReadOnlyField(source="department.code")

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "email",
            "department",
            "department_name",
            "department_code",
            "role",
            "pto_hours",
        ]


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for Assignment model with input validation."""

    employee_name = serializers.ReadOnlyField(source="employee.name")
    department_name = serializers.ReadOnlyField(source="employee.department.name")
    department_code = serializers.ReadOnlyField(source="employee.department.code")

    class Meta:
        model = Assignment
        fields = [
            "id",
            "title",
            "employee",
            "employee_name",
            "department_name",
            "department_code",
            "hours",
            "status",
        ]

    def validate_hours(self, value):
        """Field-level validation: hours cannot be negative or exceed 168 hours/week."""
        if value < 0:
            raise serializers.ValidationError("Hours cannot be negative.")
        if value > 168:
            raise serializers.ValidationError(
                "Hours cannot exceed 168 hours in a single week."
            )
        return round(float(value), 2)

    def validate_title(self, value):
        """Field-level validation: title cannot be empty or only spaces."""
        if not value or not value.strip():
            raise serializers.ValidationError("Assignment title cannot be empty.")
        return value.strip()
