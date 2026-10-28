# models.py
# Day 1: OOP - Classes, Constructors, Inheritance & Methods


class Employee:
    """Base Employee class."""

    # 1. Constructor: Initializes object attributes
    def __init__(self, name: str, department: str, weekly_capacity: float = 40.0):
        if not name:
            raise ValueError("Employee name cannot be empty!")
        if weekly_capacity <= 0:
            raise ValueError("Weekly capacity must be positive!")

        self.name: str = name
        self.department: str = department
        self.weekly_capacity: float = weekly_capacity
        self.allocated_hours: float = 0.0

    # 2. Method: Business logic attached to Employee
    def assign_hours(self, hours: float):
        """Adds hours to employee workload."""
        if hours < 0:
            raise ValueError("Cannot assign negative hours!")
        self.allocated_hours += hours

    # 3. Method: Check if employee is working overtime
    def is_overallocated(self) -> bool:
        return self.allocated_hours > self.weekly_capacity

    # 4. String representation (what prints when you print(employee))
    def __str__(self) -> str:
        return f"{self.name} ({self.department}) - {self.allocated_hours}/{self.weekly_capacity} hrs"


# 5. Inheritance: Manager inherits from Employee
class Manager(Employee):
    """Manager is an Employee with a team budget."""

    def __init__(self, name: str, department: str, team_budget_hours: float = 160.0):
        # Call the parent class constructor using super()
        super().__init__(name=name, department=department, weekly_capacity=40.0)
        self.team_budget_hours = team_budget_hours

    def __str__(self) -> str:
        return f"[Manager] {self.name} ({self.department}) - Budget: {self.team_budget_hours} hrs"


class Assignment:
    """Represents a project task assigned to an Employee."""

    def __init__(
        self, title: str, employee: Employee, hours: float, status: str = "ACTIVE"
    ):
        if hours < 0:
            raise ValueError("Hours cannot be negative!")

        self.title: str = title
        self.employee: Employee = employee
        self.hours: float = hours
        self.status: str = status.upper()

    def is_active(self) -> bool:
        return self.status == "ACTIVE"

    def __str__(self) -> str:
        return f"[{self.status}] {self.title}: {self.hours}h -> {self.employee.name}"
