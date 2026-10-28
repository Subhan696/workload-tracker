"""Day 1 Capstone Script: Filter employee assignments by department and calculate allocated hours.

Usage Examples:
    python -m day1_python.calculate_workload
    python -m day1_python.calculate_workload --department Engineering
    python -m day1_python.calculate_workload -d Product
"""

import argparse
import logging
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from .models import Assignment, Department, Employee
from .workload import (
    DepartmentNotFoundError,
    calculate_allocated_hours,
    filter_assignments_by_department,
)

# Configure logging with standard formatting
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("calculate_workload")


def get_sample_data() -> list[Assignment]:
    """Generates sample training dataset with Departments, Employees, and Assignments."""
    eng = Department(name="Engineering", code="ENG")
    pm = Department(name="Product Management", code="PM")
    qa = Department(name="Quality Assurance", code="QA")

    alice = Employee("Alice Chen", eng, weekly_capacity=40.0, pto_hours=0.0)
    bob = Employee("Bob Martinez", eng, weekly_capacity=40.0, pto_hours=8.0)
    charlie = Employee("Charlie Kim", pm, weekly_capacity=40.0, pto_hours=0.0)
    diana = Employee("Diana Prince", qa, weekly_capacity=40.0, pto_hours=4.0)

    return [
        Assignment("Workload Tracker API", alice, hours=24.0, status="ACTIVE"),
        Assignment("Auth Service Refactor", alice, hours=14.0, status="ACTIVE"),
        Assignment("UI Dashboard Widgets", bob, hours=18.0, status="ACTIVE"),
        Assignment("Legacy Migration", bob, hours=10.0, status="COMPLETED"),
        Assignment("Q3 Roadmap Planning", charlie, hours=35.0, status="ACTIVE"),
        Assignment("Integration Test Suite", diana, hours=20.0, status="ACTIVE"),
        Assignment("Bug Bash Triage", diana, hours=10.0, status="ON_HOLD"),
    ]


def print_department_report(
    department_name: str, assignments: list[Assignment]
) -> None:
    """Formats and prints a clean departmental report to stdout."""
    matched = filter_assignments_by_department(assignments, department_name)
    total_active = calculate_allocated_hours(matched, only_active=True)
    total_all = calculate_allocated_hours(matched, only_active=False)

    print("\n" + "=" * 65)
    print(f"  DEPARTMENT WORKLOAD REPORT: {department_name.upper()}")
    print("=" * 65)
    print(f" Total Assignments:       {len(matched)}")
    print(f" Active Allocated Hours:  {total_active} hrs")
    print(f" Total Allocated Hours:   {total_all} hrs")
    print("-" * 65)
    print(" [Assignments Breakdown]")
    for a in matched:
        print(f"   * {a}")
    print("-" * 65)

    # Unique employees in department
    employees = {a.employee for a in matched}
    print(" [Employee Capacities]")
    for emp in employees:
        status_flag = "[!] OVERLOADED" if emp.is_overallocated() else "[OK]"
        print(
            f"   * {emp.name:15} | Allocated: {emp.allocated_hours:4.1f}h / "
            f"{emp.net_capacity:4.1f}h | {status_flag}"
        )
    print("=" * 65 + "\n")


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Filter employee assignments by department and calculate allocated hours."
    )
    parser.add_argument(
        "-d",
        "--department",
        type=str,
        default="Engineering",
        help="Name of department to filter by (default: 'Engineering')",
    )
    return parser.parse_args()


def main() -> None:
    """Main CLI execution flow."""
    args = parse_arguments()
    assignments = get_sample_data()

    try:
        print_department_report(args.department, assignments)
    except DepartmentNotFoundError as err:
        logger.error(str(err))
        sys.exit(1)


if __name__ == "__main__":
    main()
