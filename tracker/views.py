"""API Views and ViewSets for Workload Tracker."""

from django.http import JsonResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Assignment, Department, Employee
from .permissions import IsSameDepartmentOrReadOnly
from .serializers import (
    AssignmentSerializer,
    DepartmentSerializer,
    EmployeeSerializer,
)


def health_check(request):
    """Simple API health check endpoint."""
    return JsonResponse(
        {
            "status": "healthy",
            "service": "Workload Tracker",
            "version": "1.0.0",
        }
    )


class DepartmentViewSet(viewsets.ModelViewSet):
    """API endpoint for Department CRUD."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    """API endpoint for Employee CRUD."""

    queryset = Employee.objects.select_related("department").all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Optionally filter employees by department code."""
        qs = super().get_queryset()
        dept = self.request.query_params.get("department")
        if dept:
            qs = qs.filter(department__code__iexact=dept)
        return qs


class AssignmentViewSet(viewsets.ModelViewSet):
    """API endpoint for Assignment CRUD with filtering, validation, and permissions.

    Supports:
    - GET /api/assignments/ (List with ?department=ENG & ?status=ACTIVE filters)
    - POST /api/assignments/ (Create assignment with input validation)
    - GET /api/assignments/<id>/ (Retrieve assignment details)
    - PATCH /api/assignments/<id>/ (Partial update)
    - DELETE /api/assignments/<id>/ (Delete assignment)
    """

    queryset = Assignment.objects.select_related("employee__department").all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameDepartmentOrReadOnly]

    def get_queryset(self):
        """Filters assignments by department and/or status."""
        qs = super().get_queryset()

        dept = self.request.query_params.get("department")
        if dept:
            qs = qs.filter(employee__department__code__iexact=dept)

        stat = self.request.query_params.get("status")
        if stat:
            qs = qs.filter(status__iexact=stat)

        return qs

    def perform_create(self, serializer):
        """Cross-department validation on creation for non-staff users."""
        employee = serializer.validated_data["employee"]
        user = self.request.user

        if not (user.is_staff or user.is_superuser):
            user_emp = getattr(user, "employee_profile", None)
            if user_emp and user_emp.department != employee.department:
                raise permissions.exceptions.PermissionDenied(
                    "Cannot create assignments for other departments."
                )

        serializer.save()

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Returns total active and overall allocated hours by department."""
        dept = request.query_params.get("department")
        qs = self.get_queryset()
        if dept:
            qs = qs.filter(employee__department__code__iexact=dept)

        active_hours = sum(a.hours for a in qs if a.status == "ACTIVE")
        total_hours = sum(a.hours for a in qs)

        return Response(
            {
                "department": dept or "ALL",
                "total_assignments": qs.count(),
                "active_allocated_hours": round(active_hours, 2),
                "total_allocated_hours": round(total_hours, 2),
            }
        )
