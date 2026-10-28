"""Custom permissions for Workload Tracker DRF APIs.

Implements role-based and department-level access control:
- Read-only access for all authenticated users.
- Write access (create/update/delete) restricted to staff or members of the same department.
"""

from rest_framework import permissions


class IsSameDepartmentOrReadOnly(permissions.BasePermission):
    """Object-level permission allowing updates only by users from the same department.

    Superusers and staff always have full access.
    """

    def has_permission(self, request, view):
        # All actions require authentication
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions (GET, HEAD, OPTIONS) are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Staff/Admins can edit any assignment
        if request.user.is_staff or request.user.is_superuser:
            return True

        # If user has an associated Employee profile, verify department match
        user_emp = getattr(request.user, "employee_profile", None)
        if not user_emp:
            # If user has no employee profile, check if user's username matches department code or staff
            return False

        # Verify cross-department restriction: User's department must match assignment's department
        target_department = obj.employee.department
        return user_emp.department == target_department
