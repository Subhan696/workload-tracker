"""Workload filtering and calculation services.

Demonstrates:
- Collections and list/generator comprehensions
- Functions with type hints
- Custom domain exceptions
- Named module logging
"""

import logging
from collections.abc import Sequence

from .models import Assignment

logger = logging.getLogger(__name__)


class DepartmentNotFoundError(ValueError):
    """Raised when querying a department that has no assignments or does not exist."""


def filter_assignments_by_department(
    assignments: Sequence[Assignment],
    department_name: str,
) -> list[Assignment]:
    """Filters assignments by employee's department (case-insensitive).

    Args:
        assignments: Sequence of Assignment instances.
        department_name: Name of the department to filter by.

    Returns:
        List of matching Assignment instances.

    Raises:
        DepartmentNotFoundError: If no matching assignments are found.
    """
    logger.info(f"Filtering assignments for department: '{department_name}'")

    target = department_name.strip().lower()

    # List comprehension with case-insensitive condition
    matched = [
        assignment
        for assignment in assignments
        if assignment.employee.department.strip().lower() == target
    ]

    if not matched:
        raise DepartmentNotFoundError(
            f"Department '{department_name}' not found or has no assignments."
        )

    return matched


def calculate_allocated_hours(
    assignments: Sequence[Assignment],
    only_active: bool = True,
) -> float:
    """Calculates the total allocated hours from a sequence of assignments.

    Args:
        assignments: Sequence of Assignment instances.
        only_active: If True, only sums ACTIVE assignments; otherwise sums all.

    Returns:
        Total hours rounded to 2 decimal places.
    """
    # Generator expression inside sum() for memory efficiency
    total = sum(
        assignment.hours
        for assignment in assignments
        if (not only_active or assignment.is_active())
    )
    return round(float(total), 2)


def get_department_summary(
    assignments: Sequence[Assignment],
    department_name: str,
) -> dict:
    """Generates an aggregated summary dictionary for a department."""
    dept_assignments = filter_assignments_by_department(assignments, department_name)
    active_assignments = [a for a in dept_assignments if a.is_active()]

    # Set comprehension to find unique employees
    employees = {a.employee for a in dept_assignments}

    return {
        "department": department_name,
        "total_assignments": len(dept_assignments),
        "active_assignments": len(active_assignments),
        "total_allocated_hours": calculate_allocated_hours(
            dept_assignments, only_active=False
        ),
        "active_allocated_hours": calculate_allocated_hours(
            dept_assignments, only_active=True
        ),
        "employee_count": len(employees),
        "employees": [
            {
                "name": emp.name,
                "net_capacity": emp.net_capacity,
                "allocated_hours": emp.allocated_hours,
                "is_overallocated": emp.is_overallocated(),
            }
            for emp in employees
        ],
    }
