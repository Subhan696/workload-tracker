"""Automated test suite for Day 1: Test evidence for calculations, filtering, and OOP logic."""

import pytest

from .models import Assignment, Department, Employee
from .workload import (
    DepartmentNotFoundError,
    calculate_allocated_hours,
    filter_assignments_by_department,
)


@pytest.fixture
def sample_data():
    """Test fixture providing standard departments, employees, and assignments."""
    eng = Department("Engineering", "ENG")
    qa = Department("Quality Assurance", "QA")

    emp_alice = Employee("Alice", eng, weekly_capacity=40.0, pto_hours=0.0)
    emp_bob = Employee(
        "Bob", eng, weekly_capacity=40.0, pto_hours=8.0
    )  # Net capacity = 32.0
    emp_charlie = Employee("Charlie", qa, weekly_capacity=40.0, pto_hours=0.0)

    assignments = [
        Assignment("Task 1", emp_alice, hours=20.0, status="ACTIVE"),
        Assignment("Task 2", emp_alice, hours=15.0, status="ACTIVE"),
        Assignment(
            "Task 3", emp_bob, hours=35.0, status="ACTIVE"
        ),  # Overallocated (35 > 32)
        Assignment("Task 4", emp_bob, hours=10.0, status="COMPLETED"),
        Assignment("Task 5", emp_charlie, hours=25.0, status="ACTIVE"),
    ]

    return {
        "eng": eng,
        "qa": qa,
        "alice": emp_alice,
        "bob": emp_bob,
        "charlie": emp_charlie,
        "assignments": assignments,
    }


def test_filter_assignments_by_department_success(sample_data):
    """Verifies filtering returns only assignments matching the requested department."""
    assignments = sample_data["assignments"]
    matched = filter_assignments_by_department(assignments, "Engineering")
    assert len(matched) == 4
    for a in matched:
        assert a.employee.department == "Engineering"


def test_filter_assignments_case_insensitive(sample_data):
    """Verifies department filtering works case-insensitively."""
    assignments = sample_data["assignments"]
    matched = filter_assignments_by_department(assignments, "engineering")
    assert len(matched) == 4


def test_filter_assignments_nonexistent_department_raises_error(sample_data):
    """Verifies that an unknown department raises DepartmentNotFoundError."""
    assignments = sample_data["assignments"]
    with pytest.raises(DepartmentNotFoundError) as exc_info:
        filter_assignments_by_department(assignments, "Marketing")
    assert "Marketing" in str(exc_info.value)


def test_calculate_allocated_hours_active_only(sample_data):
    """Verifies summing only active assignments."""
    eng_assignments = filter_assignments_by_department(
        sample_data["assignments"], "Engineering"
    )
    # Task 1 (20) + Task 2 (15) + Task 3 (35) = 70 (Task 4 is COMPLETED, so ignored)
    active_hours = calculate_allocated_hours(eng_assignments, only_active=True)
    assert active_hours == 70.0


def test_calculate_allocated_hours_all(sample_data):
    """Verifies summing all assignments including COMPLETED."""
    eng_assignments = filter_assignments_by_department(
        sample_data["assignments"], "Engineering"
    )
    total_hours = calculate_allocated_hours(eng_assignments, only_active=False)
    assert total_hours == 80.0


def test_employee_overallocation_logic(sample_data):
    """Verifies that employee net capacity and overload status are correctly calculated."""
    alice = sample_data["alice"]
    bob = sample_data["bob"]

    assert alice.net_capacity == 40.0
    assert not alice.is_overallocated()  # 35 <= 40

    assert bob.net_capacity == 32.0  # 40 - 8 PTO
    assert bob.is_overallocated()  # 35 > 32
