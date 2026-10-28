"""Day 3 Live API Demonstration Script.

Demonstrates:
1. Unauthenticated Request -> 401 Unauthorized
2. Authenticated GET /api/assignments/ -> 200 OK
3. Filter by department (?department=ENG) -> 200 OK
4. POST new assignment with valid data -> 201 Created
5. POST assignment with invalid hours (-10h) -> 400 Bad Request
6. PATCH assignment hours -> 200 OK
7. Unauthorized cross-department edit attempt -> 403 Forbidden
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tracker.models import Assignment, Department, Employee


def setup_demo_users_and_data():
    """Ensures test users, departments, and employees exist."""
    eng, _ = Department.objects.get_or_create(name="Engineering", code="ENG")
    pm, _ = Department.objects.get_or_create(name="Product Management", code="PM")

    admin_user, _ = User.objects.get_or_create(
        username="admin_lead", defaults={"is_staff": True, "is_superuser": True}
    )
    admin_user.set_password("admin123")
    admin_user.save()

    eng_user, _ = User.objects.get_or_create(username="alice_eng")
    eng_user.set_password("pass123")
    eng_user.save()

    pm_user, _ = User.objects.get_or_create(username="charlie_pm")
    pm_user.set_password("pass123")
    pm_user.save()

    alice, _ = Employee.objects.get_or_create(
        email="alice@devsinc.com",
        defaults={
            "name": "Alice Chen",
            "department": eng,
            "user": eng_user,
            "role": "Senior Engineer",
        },
    )
    if not alice.user:
        alice.user = eng_user
        alice.save()

    charlie, _ = Employee.objects.get_or_create(
        email="charlie@devsinc.com",
        defaults={
            "name": "Charlie Kim",
            "department": pm,
            "user": pm_user,
            "role": "Product Manager",
        },
    )
    if not charlie.user:
        charlie.user = pm_user
        charlie.save()

    assignment, _ = Assignment.objects.get_or_create(
        title="Workload Tracker API",
        defaults={"employee": alice, "hours": 24.0, "status": "ACTIVE"},
    )

    return admin_user, eng_user, pm_user, alice, assignment


def run_live_api_demo():
    admin_user, eng_user, pm_user, alice, assignment = setup_demo_users_and_data()
    client = APIClient()

    print("=" * 70)
    print("  DAY 3: DRF APIS, AUTHENTICATION & PERMISSIONS DEMO")
    print("=" * 70)

    # 1. Unauthenticated Request -> 401/403
    print("\n[1. Unauthenticated Request]")
    r = client.get("/api/assignments/")
    print(
        f"   GET /api/assignments/ -> Status: {r.status_code} (Expected: 401/403 Rejected)"
    )
    print(f"   Response: {r.data}")

    # 2. Authenticated GET Request
    client.force_authenticate(user=eng_user)
    print("\n[2. Authenticated GET (User: alice_eng)]")
    r = client.get("/api/assignments/")
    print(f"   GET /api/assignments/ -> Status: {r.status_code} OK")
    results = r.data.get("results", r.data)
    print(f"   Total Returned: {len(results)} assignments")

    # 3. Filter by department
    print("\n[3. Filtering by Department (?department=ENG)]")
    r = client.get("/api/assignments/?department=ENG")
    results = r.data.get("results", r.data)
    print(f"   GET /api/assignments/?department=ENG -> Status: {r.status_code}")
    for item in results[:2]:
        print(
            f"   * [{item['status']}] {item['title']} ({item['hours']}h) - Dept: {item['department_code']}"
        )

    # 4. POST with invalid hours -> 400 Bad Request
    print("\n[4. Input Validation Error: Hours = -15.0]")
    r = client.post(
        "/api/assignments/",
        {"title": "Bad Task", "employee": alice.id, "hours": -15.0, "status": "ACTIVE"},
    )
    print(
        f"   POST /api/assignments/ -> Status: {r.status_code} (Expected: 400 Bad Request)"
    )
    print(f"   Error Detail: {r.data}")

    # 5. POST with valid data
    client.force_authenticate(user=admin_user)
    print("\n[5. POST New Assignment (Valid Input)]")
    r = client.post(
        "/api/assignments/",
        {
            "title": "Live Demo Task",
            "employee": alice.id,
            "hours": 20.0,
            "status": "ACTIVE",
        },
    )
    print(f"   POST /api/assignments/ -> Status: {r.status_code} Created")
    print(
        f"   Created Assignment: ID {r.data.get('id')} - {r.data.get('title')} ({r.data.get('hours')}h)"
    )

    # 6. PATCH update
    client.force_authenticate(user=eng_user)
    print("\n[6. PATCH Assignment (Same Department)]")
    r = client.patch(f"/api/assignments/{assignment.id}/", {"hours": 26.0})
    print(f"   PATCH /api/assignments/{assignment.id}/ -> Status: {r.status_code} OK")
    print(f"   Updated Hours: {r.data.get('hours')}h")

    # 7. Cross-department unauthorized edit -> 403 Forbidden
    client.force_authenticate(user=pm_user)  # charlie_pm from PM department!
    print(
        "\n[7. Cross-Department Unauthorized Edit (User: charlie_pm from PM trying to edit ENG task)]"
    )
    r = client.patch(f"/api/assignments/{assignment.id}/", {"hours": 50.0})
    print(
        f"   PATCH /api/assignments/{assignment.id}/ -> Status: {r.status_code} (Expected: 403 Forbidden)"
    )
    print(f"   Access Denied Response: {r.data}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_live_api_demo()
