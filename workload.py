# workload.py
import logging

from models import Assignment

logger = logging.getLogger(__name__)


def filter_assignments_by_department(
    assignments: list[Assignment], dept_name: str
) -> list[Assignment]:
    """Filters assignments by employee's department (case-insensitive)."""
    logger.info(f"Filtering assignments for department: {dept_name}")

    target = dept_name.strip().lower()
    matched = [
        a for a in assignments if a.employee.department.strip().lower() == target
    ]

    if not matched:
        raise ValueError(f"No assignments found for department '{dept_name}'!")

    return matched


def calculate_allocated_hours(
    assignments: list[Assignment], only_active: bool = True
) -> float:
    """Calculates total hours for the given assignments."""
    if only_active:
        return sum(a.hours for a in assignments if a.is_active())
    return sum(a.hours for a in assignments)
