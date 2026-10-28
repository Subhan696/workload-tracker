"""Domain models for Day 1: Demonstrates OOP, Constructors, Inheritance, and Methods."""


class Department:
    """Represents an organization department."""

    def __init__(self, name: str, code: str):
        if not name or not name.strip():
            raise ValueError("Department name cannot be empty.")
        if not code or not code.strip():
            raise ValueError("Department code cannot be empty.")

        self.name: str = name.strip()
        self.code: str = code.strip().upper()

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    def __repr__(self) -> str:
        return f"Department(code={self.code!r}, name={self.name!r})"


class Employee:
    """Base Employee class."""

    def __init__(
        self,
        name: str,
        department: Department | str,
        weekly_capacity: float = 40.0,
        pto_hours: float = 0.0,
    ):
        if not name or not name.strip():
            raise ValueError("Employee name cannot be empty.")
        if weekly_capacity <= 0:
            raise ValueError("Weekly capacity must be positive.")

        self.name: str = name.strip()
        self.department: str = (
            department.name
            if isinstance(department, Department)
            else str(department).strip()
        )
        self.weekly_capacity: float = float(weekly_capacity)
        self.pto_hours: float = max(0.0, float(pto_hours))
        self.allocated_hours: float = 0.0

    @property
    def net_capacity(self) -> float:
        """Effective capacity after subtracting PTO."""
        return max(0.0, self.weekly_capacity - self.pto_hours)

    def assign_hours(self, hours: float) -> None:
        """Adds allocated hours to employee workload."""
        if hours < 0:
            raise ValueError("Cannot assign negative hours.")
        self.allocated_hours += hours

    def is_overallocated(self) -> bool:
        """Checks if employee's allocated hours exceed their net capacity."""
        return self.allocated_hours > self.net_capacity

    def __str__(self) -> str:
        return f"{self.name} ({self.department}) - {self.allocated_hours}/{self.net_capacity} hrs"


class Manager(Employee):
    """Manager inherits from Employee with an added team budget."""

    def __init__(
        self,
        name: str,
        department: Department | str,
        team_budget_hours: float = 160.0,
    ):
        super().__init__(name=name, department=department, weekly_capacity=40.0)
        self.team_budget_hours: float = float(team_budget_hours)

    def __str__(self) -> str:
        return f"[Manager] {self.name} ({self.department}) - Budget: {self.team_budget_hours}h"


class Assignment:
    """Represents a project workload allocation assigned to an Employee."""

    def __init__(
        self,
        title: str,
        employee: Employee,
        hours: float,
        status: str = "ACTIVE",
    ):
        if not title or not title.strip():
            raise ValueError("Assignment title cannot be empty.")
        if hours < 0 or hours > 168:
            raise ValueError(f"Invalid hours ({hours}): must be between 0 and 168.")

        self.title: str = title.strip()
        self.employee: Employee = employee
        self.hours: float = round(float(hours), 2)
        self.status: str = status.strip().upper()

        # Update the employee's internal counter if active
        if self.is_active():
            self.employee.assign_hours(self.hours)

    def is_active(self) -> bool:
        """Checks if the assignment actively consumes weekly hours."""
        return self.status == "ACTIVE"

    def __str__(self) -> str:
        return f"[{self.status}] {self.title}: {self.hours}h -> {self.employee.name}"
