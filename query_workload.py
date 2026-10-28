"""Day 2 ORM Script: Demonstrates CRUD, filtering, Q objects, select_related, and SQL inspection.

Usage:
    python query_workload.py
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1. Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.db.models import Q

from tracker.models import Assignment, Department, Employee


def seed_database_if_empty() -> None:
    """Populates initial sample training records if none exist."""
    if Department.objects.exists():
        return

    print(">>> Database is empty. Seeding initial training data...")
    eng = Department.objects.create(name="Engineering", code="ENG")
    pm = Department.objects.create(name="Product Management", code="PM")
    qa = Department.objects.create(name="Quality Assurance", code="QA")

    alice = Employee.objects.create(
        name="Alice Chen",
        email="alice@devsinc.com",
        department=eng,
        role="Senior Backend Engineer",
        pto_hours=0.0,
    )
    bob = Employee.objects.create(
        name="Bob Martinez",
        email="bob@devsinc.com",
        department=eng,
        role="Full-Stack Engineer",
        pto_hours=8.0,
    )
    charlie = Employee.objects.create(
        name="Charlie Kim",
        email="charlie@devsinc.com",
        department=pm,
        role="Product Manager",
        pto_hours=0.0,
    )
    diana = Employee.objects.create(
        name="Diana Prince",
        email="diana@devsinc.com",
        department=qa,
        role="QA Automation Lead",
        pto_hours=4.0,
    )

    Assignment.objects.create(
        title="Workload API", employee=alice, hours=24.0, status="ACTIVE"
    )
    Assignment.objects.create(
        title="Auth Service Refactor", employee=alice, hours=14.0, status="ACTIVE"
    )
    Assignment.objects.create(
        title="UI Dashboard Widgets", employee=bob, hours=18.0, status="ACTIVE"
    )
    Assignment.objects.create(
        title="Legacy Code Migration", employee=bob, hours=10.0, status="COMPLETED"
    )
    Assignment.objects.create(
        title="Q3 Roadmap Planning", employee=charlie, hours=35.0, status="ACTIVE"
    )
    Assignment.objects.create(
        title="Integration Test Suite", employee=diana, hours=20.0, status="ACTIVE"
    )
    Assignment.objects.create(
        title="Bug Triage Review", employee=diana, hours=8.0, status="ON_HOLD"
    )
    print(">>> Database seeded successfully!\n")


def demonstrate_orm_queries() -> None:
    """Demonstrates all Day 2 ORM query patterns."""
    seed_database_if_empty()

    print("=" * 70)
    print("  DAY 2: DJANGO ORM DEMO & QUERY INSPECTION")
    print("=" * 70)

    # 1. Exercise Requirement: Query by Department and Assignment Status
    print("\n[1. EXERCISE: Filter by Department ('ENG') and Status ('ACTIVE')]")
    eng_active = Assignment.objects.filter(
        employee__department__code="ENG", status="ACTIVE"
    )
    for a in eng_active:
        print(
            f"   * {a.title} ({a.hours}h) -> {a.employee.name} [{a.employee.department.code}]"
        )

    # 2. SQL Inspection: See the raw SQL Django generates
    print("\n[2. SQL QUERY INSPECTION]")
    print(f"   SQL: {eng_active.query}")

    # 3. Q Objects: Complex OR queries
    print("\n[3. Q OBJECTS: Status is COMPLETED OR Hours >= 20]")
    q_filter = Assignment.objects.filter(Q(status="COMPLETED") | Q(hours__gte=20.0))
    for a in q_filter:
        print(f"   * [{a.status}] {a.title} ({a.hours}h) -> {a.employee.name}")

    # 4. select_related: Single-query SQL JOIN (Fixes N+1 problem)
    print(
        "\n[4. SELECT_RELATED: Fetches Assignment + Employee + Department in 1 SQL JOIN]"
    )
    fast_assignments = Assignment.objects.select_related("employee__department").all()
    for a in fast_assignments[:3]:
        print(
            f"   * {a.title} | {a.employee.name} | Dept: {a.employee.department.name}"
        )

    # 5. prefetch_related: Reverse relation (Department -> all Employees)
    print("\n[5. PREFETCH_RELATED: Reverse lookup (Department -> Employees)]")
    departments = Department.objects.prefetch_related("employees").all()
    for d in departments:
        emp_names = [e.name for e in d.employees.all()]
        print(f"   * {d.name} ({len(emp_names)} members): {', '.join(emp_names)}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    demonstrate_orm_queries()
