"""Day 5 Full-Stack Capstone End-to-End Verification Script.

Demonstrates and verifies:
1. Combined Department & Status filtering (?department=ENG&status=ACTIVE)
2. Cross-Department Creation Permission check (Alice -> PM: 403 Forbidden)
3. Same-Department Creation (Alice -> ENG: 201 Created)
4. Field Validation (hours = -10.0 -> 400 Bad Request)
5. Full-Stack Data Flow: PATCH status & hours update (200 OK)
6. Department Workload Summary Aggregation (/api/assignments/summary/)
7. Admin Override Access Control
"""

import os
import sys

# Ensure UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from tracker.models import Assignment, Department, Employee


def run_fullstack_e2e_tests():
    client = APIClient()

    eng = Department.objects.get(code="ENG")
    pm = Department.objects.get(code="PM")

    user_alice = User.objects.get(username="alice_eng")
    user_charlie = User.objects.get(username="charlie_pm")
    user_admin = User.objects.get(username="admin_lead")

    emp_alice = Employee.objects.get(user=user_alice)
    emp_charlie = Employee.objects.get(user=user_charlie)
    emp_bob = Employee.objects.get(name="Bob Martinez")

    print("=" * 72)
    print("  DAY 5: FULL-STACK CAPSTONE END-TO-END VERIFICATION")
    print("=" * 72)

    # 1. Combined Filter: Department=ENG & Status=ACTIVE
    print("\n[Test 1: Combined Filter (?department=ENG&status=ACTIVE)]")
    client.force_authenticate(user=user_alice)
    res = client.get("/api/assignments/?department=ENG&status=ACTIVE")
    print(f"   GET /api/assignments/?department=ENG&status=ACTIVE -> Status: {res.status_code}")
    results = res.data.get("results", res.data)
    print(f"   Active ENG Assignments Count: {len(results)}")
    for a in results[:3]:
        print(f"   - #{a['id']} {a['title']} ({a['hours']}h) [{a['status']}] - Dept: {a['department_code']}")
    assert res.status_code == status.HTTP_200_OK

    # 2. Cross-Department Creation Permission Check
    print("\n[Test 2: Cross-Department Creation Rejection (Alice [ENG] -> Charlie [PM])]")
    res_cross = client.post(
        "/api/assignments/",
        {
            "title": "Unauthorized PM Feature",
            "employee": emp_charlie.id,
            "hours": 15.0,
            "status": "ACTIVE",
        },
        format="json",
    )
    print(f"   POST /api/assignments/ (Cross-Dept) -> Status: {res_cross.status_code} (Expected: 403 Forbidden)")
    print(f"   Response Detail: {res_cross.data.get('detail')}")
    assert res_cross.status_code == status.HTTP_403_FORBIDDEN

    # 3. Same-Department Creation (Valid)
    print("\n[Test 3: Same-Department Creation (Alice [ENG] -> Bob [ENG])]")
    res_valid = client.post(
        "/api/assignments/",
        {
            "title": "Day 5 Capstone Verification Task",
            "employee": emp_bob.id,
            "hours": 18.0,
            "status": "ACTIVE",
        },
        format="json",
    )
    print(f"   POST /api/assignments/ -> Status: {res_valid.status_code} (Expected: 201 Created)")
    new_assignment_id = res_valid.data["id"]
    print(f"   Created Assignment: ID #{new_assignment_id} - '{res_valid.data['title']}' ({res_valid.data['hours']}h)")
    assert res_valid.status_code == status.HTTP_201_CREATED

    # 4. Input Validation (Negative Hours)
    print("\n[Test 4: Input Validation (Hours = -10.0)]")
    res_invalid = client.post(
        "/api/assignments/",
        {
            "title": "Invalid Negative Task",
            "employee": emp_alice.id,
            "hours": -10.0,
            "status": "ACTIVE",
        },
        format="json",
    )
    print(f"   POST /api/assignments/ (hours: -10) -> Status: {res_invalid.status_code} (Expected: 400 Bad Request)")
    print(f"   Validation Error: {res_invalid.data}")
    assert res_invalid.status_code == status.HTTP_400_BAD_REQUEST

    # 5. Full-Stack Data Flow: PATCH Status & Hours Update
    print(f"\n[Test 5: Full Data-Flow Update (PATCH /api/assignments/{new_assignment_id}/)]")
    res_patch = client.patch(
        f"/api/assignments/{new_assignment_id}/",
        {"status": "COMPLETED", "hours": 20.0},
        format="json",
    )
    print(f"   PATCH /api/assignments/{new_assignment_id}/ -> Status: {res_patch.status_code} OK")
    print(f"   Updated Status: {res_patch.data['status']}, Updated Hours: {res_patch.data['hours']}h")
    assert res_patch.status_code == status.HTTP_200_OK
    assert res_patch.data["status"] == "COMPLETED"
    assert res_patch.data["hours"] == 20.0

    # 6. Workload Summary Aggregation Check
    print("\n[Test 6: Department Workload Summary Aggregation]")
    res_summary = client.get("/api/assignments/summary/?department=ENG")
    print(f"   GET /api/assignments/summary/?department=ENG -> Status: {res_summary.status_code}")
    print(f"   Aggregated Metrics: {res_summary.data}")
    assert res_summary.status_code == status.HTTP_200_OK

    # 7. Admin Override Access
    print("\n[Test 7: Staff/Admin Cross-Department Override]")
    client.force_authenticate(user=user_admin)
    res_admin = client.post(
        "/api/assignments/",
        {
            "title": "Admin Mandated PM Initiative",
            "employee": emp_charlie.id,
            "hours": 12.0,
            "status": "ACTIVE",
        },
        format="json",
    )
    print(f"   POST /api/assignments/ by Admin -> Status: {res_admin.status_code} (Expected: 201 Created)")
    assert res_admin.status_code == status.HTTP_201_CREATED

    print("\n" + "=" * 72)
    print("  ALL 7 DAY 5 FULL-STACK CAPSTONE TESTS PASSED SUCCESSFULLY! ")
    print("=" * 72)


if __name__ == "__main__":
    run_fullstack_e2e_tests()
