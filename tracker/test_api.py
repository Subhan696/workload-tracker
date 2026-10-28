"""Automated API test suite for Day 3 DRF endpoints, validation, and permissions.

Verifies:
1. Unauthenticated requests (401 Unauthorized)
2. GET assignments and filtering by department/status
3. POST assignment with valid data (201 Created)
4. POST assignment with invalid hours/input (400 Bad Request)
5. PATCH assignment update (200 OK)
6. Unauthorized cross-department modification (403 Forbidden)
"""

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Assignment, Department, Employee


class AssignmentAPITests(APITestCase):
    """Test suite for /api/assignments/ endpoints."""

    def setUp(self):
        """Sets up test departments, users, employee profiles, and sample assignments."""
        self.dept_eng = Department.objects.create(name="Engineering", code="ENG")
        self.dept_pm = Department.objects.create(name="Product Management", code="PM")

        # Staff Admin user
        self.admin_user = User.objects.create_superuser(
            username="admin_user", email="admin@test.com", password="password123"
        )

        # Engineering Employee User
        self.user_eng = User.objects.create_user(
            username="alice_eng", email="alice@test.com", password="password123"
        )
        self.emp_alice = Employee.objects.create(
            user=self.user_eng,
            name="Alice Chen",
            email="alice@test.com",
            department=self.dept_eng,
            role="Backend Engineer",
        )

        # Product Employee User (Different department!)
        self.user_pm = User.objects.create_user(
            username="charlie_pm", email="charlie@test.com", password="password123"
        )
        self.emp_charlie = Employee.objects.create(
            user=self.user_pm,
            name="Charlie Kim",
            email="charlie@test.com",
            department=self.dept_pm,
            role="Product Manager",
        )

        # Engineering Assignment
        self.assignment_eng = Assignment.objects.create(
            title="Workload Tracker API",
            employee=self.emp_alice,
            hours=20.0,
            status="ACTIVE",
        )

        # PM Assignment
        self.assignment_pm = Assignment.objects.create(
            title="Roadmap Q3",
            employee=self.emp_charlie,
            hours=15.0,
            status="ACTIVE",
        )

        self.list_url = "/api/assignments/"
        self.detail_url_eng = f"/api/assignments/{self.assignment_eng.id}/"

    def test_unauthenticated_request_fails(self):
        """Verifies unauthenticated requests are rejected (401 or 403)."""
        response = self.client.get(self.list_url)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

        # Explicit invalid token header returns 401 Unauthorized or 403 Forbidden
        response_invalid_token = self.client.get(
            self.list_url, HTTP_AUTHORIZATION="Token invalid_token_12345"
        )
        self.assertIn(
            response_invalid_token.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_authenticated_get_assignments_list(self):
        """Verifies authenticated users can list assignments."""
        self.client.force_authenticate(user=self.user_eng)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Results can be in results list (if paginated) or root list
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 2)

    def test_filter_assignments_by_department(self):
        """Verifies filtering assignments by department query parameter (?department=ENG)."""
        self.client.force_authenticate(user=self.user_eng)
        response = self.client.get(f"{self.list_url}?department=ENG")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Workload Tracker API")

    def test_post_assignment_valid_data(self):
        """Verifies creating an assignment with valid input returns 201 Created."""
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "title": "New Microservice",
            "employee": self.emp_alice.id,
            "hours": 30.0,
            "status": "ACTIVE",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Microservice")
        self.assertEqual(response.data["hours"], 30.0)

    def test_post_assignment_invalid_negative_hours(self):
        """Verifies serializer validation rejects negative hours with 400 Bad Request."""
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "title": "Invalid Task",
            "employee": self.emp_alice.id,
            "hours": -10.0,
            "status": "ACTIVE",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("hours", response.data)

    def test_post_assignment_invalid_excessive_hours(self):
        """Verifies serializer validation rejects hours > 168 with 400 Bad Request."""
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "title": "Impossible Task",
            "employee": self.emp_alice.id,
            "hours": 200.0,
            "status": "ACTIVE",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("hours", response.data)

    def test_patch_assignment_success_for_same_department(self):
        """Verifies an employee can update an assignment in their own department (200 OK)."""
        self.client.force_authenticate(user=self.user_eng)
        payload = {"hours": 28.0}
        response = self.client.patch(self.detail_url_eng, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["hours"], 28.0)

    def test_patch_assignment_unauthorized_cross_department_forbidden(self):
        """Verifies cross-department modification is blocked with 403 Forbidden."""
        # user_pm (Product) attempts to modify assignment_eng (Engineering)
        self.client.force_authenticate(user=self.user_pm)
        payload = {"hours": 50.0}
        response = self.client.patch(self.detail_url_eng, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
