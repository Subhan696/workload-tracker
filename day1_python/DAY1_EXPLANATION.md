# Day 1: Workload Tracker Architecture & 5-Minute Demo Guide

This document is your complete walkthrough to explain **Day 1** to your mentor, team lead, or evaluator.

---

## 1. High-Level Summary (The 30-Second Elevator Pitch)
> "In Day 1, we set up a professional full-stack development environment with clean Git hygiene and built the core domain logic for the Workload Tracker. We modeled Departments, Employees, and Assignments using Object-Oriented Programming (OOP), implemented memory-efficient comprehensions to filter assignments and calculate workload hours, and wrapped the solution in a modular CLI script with automated unit tests and strict formatting via Black and Ruff."

---

## 2. Walkthrough of the 5 Core Blocks

### Block 1: Environment & Dependency Hygiene
- **Virtual Environment (`.venv`):** Isolates our project dependencies so we never pollute the global Python runtime.
- **Git Shield (`.gitignore`):** Explicitly ignores `.venv/`, `.env`, `db.sqlite3`, and `__pycache__/` to guarantee zero credentials or binary garbage are ever committed.
- **12-Factor App Configuration:** Kept configuration in `.env` (ignored) and provided `.env.example` as a template for teammates.
- **Production vs Dev Dependencies:** Separated runtime requirements (`requirements.txt`) from linter/test tools (`requirements-dev.txt`).

### Block 2: Collections & Comprehensions
- **Comprehensions vs For-Loops:** Instead of verbose 5-line imperative for-loops, we used Pythonic list comprehensions:
  ```python
  matched = [a for a in assignments if a.employee.department.lower() == target]
  ```
- **Generator Summation:** Computed total allocated hours efficiently:
  ```python
  total_hours = sum(a.hours for a in assignments if a.is_active())
  ```
- **Set Comprehensions:** Gathered distinct employees and unique departments using `{a.employee for a in matched}`.

### Block 3: Functions, Type Hints, Exceptions & Logging
- **Type Hints:** Self-documenting function signatures using `list[Assignment]`, `str`, and `float`.
- **Domain Exceptions:** Custom `DepartmentNotFoundError` instead of generic silent failures.
- **Structured Logging:** Configured `logger = logging.getLogger(__name__)` to attach module names, timestamps, and log levels to output messages.

### Block 4: Object-Oriented Programming (OOP)
- **`Department`:** Encapsulates department name and code.
- **`Employee`:** Manages employee capacity, PTO hours deduction (`net_capacity`), and workload assignment tracking.
- **`Manager(Employee)`:** Demonstrates OOP **Inheritance** by extending `Employee` with `super().__init__()` and adding team budget tracking.
- **`Assignment`:** Validates reasonable weekly hours (0–168), tracks status (`ACTIVE`, `COMPLETED`, `ON_HOLD`), and auto-increments employee workload.

### Block 5: The Capstone Script, Testing & Git
- **Modular CLI Tool (`calculate_workload.py`):** Accepts `--department` flags, filters assignments, and displays a formatted workload capacity report.
- **Automated Tests (`test_workload.py`):** 6 test cases verifying active hours summation, case-insensitive filtering, exception raising, and employee overload detection.
- **Code Quality:** 100% formatted with `black` and linted with `ruff`.
- **Git Branching:** Work committed to isolated feature branch `feature/day1-python-workload` with conventional commit messages.

---

## 3. How to Demonstrate Live (Terminal Commands)

### A. Run the CLI Tool:
```powershell
python -m day1_python.calculate_workload --department Engineering
```

### B. Run the Automated Tests:
```powershell
pytest day1_python/test_workload.py -v
```

### C. Demonstrate Lint Compliance:
```powershell
ruff check day1_python
black --check day1_python
```

---

## 4. Common Questions & Answers for Your Demo

**Q: Why use list comprehensions instead of regular loops?**  
*A: List comprehensions are more concise, readable, and in CPython, they execute faster because the loop bytecode is optimized in C.*

**Q: Why did we use `getLogger(__name__)` instead of `logging.info()` directly?**  
*A: Calling methods on the root logger obscures which module originated the message. `getLogger(__name__)` scopes messages to `day1_python.workload`, making debugging across multi-file applications clean.*

**Q: How does `Manager` reuse `Employee` logic?**  
*A: Through inheritance. By invoking `super().__init__(name=name, department=department)`, `Manager` inherits all properties and methods of `Employee` (like `assign_hours` and `is_overallocated`) without duplicating code.*
