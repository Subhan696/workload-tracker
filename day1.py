# day1.py
# Day 1 Capstone: Filter employee assignments by department and calculate allocated hours
import logging

from models import Assignment, Employee
from workload import calculate_allocated_hours, filter_assignments_by_department

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    # 1. Create Employees
    alice = Employee("Alice Chen", "Engineering")
    bob = Employee("Bob Martinez", "Engineering")
    charlie = Employee("Charlie Kim", "Product")

    # 2. Create Assignments
    assignments = [
        Assignment("Workload API", alice, hours=24.0, status="ACTIVE"),
        Assignment("Auth Service", alice, hours=14.0, status="ACTIVE"),
        Assignment("UI Dashboard", bob, hours=18.0, status="ACTIVE"),
        Assignment("Old Code Migration", bob, hours=10.0, status="COMPLETED"),
        Assignment("Roadmap Planning", charlie, hours=30.0, status="ACTIVE"),
    ]

    # 3. Filter and Calculate for Engineering
    target_dept = "Engineering"
    try:
        matched = filter_assignments_by_department(assignments, target_dept)
        total_hours = calculate_allocated_hours(matched, only_active=True)

        print("\n" + "=" * 50)
        print(f" Department Report: {target_dept}")
        print("=" * 50)
        for a in matched:
            print(f" - {a}")
        print("-" * 50)
        print(f" Total Active Allocated Hours: {total_hours} hrs\n")

    except ValueError as err:
        logger.error(err)


if __name__ == "__main__":
    main()
