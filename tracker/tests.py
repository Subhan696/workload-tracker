"""Unit tests for Day 2 Django Models, Views, and ORM Queries."""

from django.test import Client, TestCase

from .models import Assignment, Department, Employee


class TrackerModelTests(TestCase):
    """Tests Department, Employee, and Assignment ORM models and queries."""

    def setUp(self):
        """Set up test departments, employees, and assignments."""
        self.dept_eng = Department.objects.create(name="Engineering", code="ENG")
        self.dept_qa = Department.objects.create(name="Quality Assurance", code="QA")

        self.emp_alice = Employee.objects.create(
            name="Alice Chen",
            email="alice@test.com",
            department=self.dept_eng,
            pto_hours=0.0,
        )
        self.emp_bob = Employee.objects.create(
            name="Bob Martinez",
            email="bob@test.com",
            department=self.dept_eng,
            pto_hours=8.0,
        )
        self.emp_charlie = Employee.objects.create(
            name="Charlie Kim",
            email="charlie@test.com",
            department=self.dept_qa,
            pto_hours=0.0,
        )

        self.assignment_1 = Assignment.objects.create(
            title="Workload API", employee=self.emp_alice, hours=24.0, status="ACTIVE"
        )
        self.assignment_2 = Assignment.objects.create(
            title="Auth Service", employee=self.emp_alice, hours=14.0, status="ACTIVE"
        )
        self.assignment_3 = Assignment.objects.create(
            title="UI Widgets", employee=self.emp_bob, hours=18.0, status="ACTIVE"
        )
        self.assignment_4 = Assignment.objects.create(
            title="Old Migration", employee=self.emp_bob, hours=10.0, status="COMPLETED"
        )

    def test_department_str(self):
        """Verifies department string representation."""
        self.assertEqual(str(self.dept_eng), "Engineering (ENG)")

    def test_employee_relationship(self):
        """Verifies reverse foreign key relationship from Department to Employees."""
        self.assertEqual(self.dept_eng.employees.count(), 2)

    def test_query_by_department_and_status(self):
        """Verifies Day 2 exercise: querying assignments by department code and active status."""
        eng_active = Assignment.objects.filter(
            employee__department__code="ENG", status="ACTIVE"
        )
        self.assertEqual(eng_active.count(), 3)
        titles = list(eng_active.values_list("title", flat=True))
        self.assertIn("Workload API", titles)
        self.assertIn("Auth Service", titles)
        self.assertIn("UI Widgets", titles)
        self.assertNotIn("Old Migration", titles)

    def test_health_check_view(self):
        """Verifies /api/health/ returns status 200 and healthy JSON."""
        client = Client()
        response = client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "Workload Tracker")
