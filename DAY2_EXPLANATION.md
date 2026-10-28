# Day 2: Django Models, Database Access & 5-Minute Demo Guide

This document is your complete walkthrough to explain **Day 2** to your mentor, team lead, or evaluator.

---

## 1. High-Level Summary (The 30-Second Elevator Pitch)
> "In Day 2, we transitioned our in-memory Python data into a database-backed web application using the Django Framework. We generated a production Django project and app structure, configured URL routing and JSON views, designed relational database models (`Department`, `Employee`, `Assignment`) using Django ORM with ForeignKeys, executed safe schema migrations, and mastered query optimization—including `Q` objects, `select_related` to eliminate N+1 queries, and registered our models with search and filters in the Django Admin portal."

---

## 2. Walkthrough of the 5 Core Blocks

### Block 1: Django Architecture, Settings, URLs & Views
- **Project vs App:** `config/` is the project brain (global settings, database connection, root URLs), while `tracker/` is the focused application module.
- **`settings.py` Registration:** Added `'tracker'` to `INSTALLED_APPS` so Django recognizes our models and views.
- **Request / Response Flow:**
  - Browser/Client requests `/api/health/`.
  - Root `config/urls.py` routes the prefix `/api/` to `tracker/urls.py`.
  - `tracker/views.py` executes the `health_check` function and returns a `JsonResponse({"status": "healthy"})`.

### Block 2: ORM Models, Fields & ForeignKeys
- **`Department`:** `name` and `code` (unique constraint).
- **`Employee`:** `name`, `email`, `role`, `pto_hours`, and a `ForeignKey` to `Department` with `on_delete=models.CASCADE` and `related_name="employees"`.
- **`Assignment`:** `title`, `hours`, `status` (`TextChoices`: `ACTIVE`, `COMPLETED`, `ON_HOLD`), and a `ForeignKey` to `Employee`.
- **`related_name` Advantage:** Allows reverse querying. For example, `department.employees.all()` retrieves all team members without writing custom queries.

### Block 3: Migrations & Schema Safety
- **2-Step Migration Lifecycle:**
  1. `python manage.py makemigrations tracker`: Generates a version-controlled Python blueprint (`0001_initial.py`).
  2. `python manage.py migrate`: Executes SQL `CREATE TABLE` and schema constraints safely against SQLite (`db.sqlite3`).
- **SQL Inspection (`sqlmigrate`):** Running `python manage.py sqlmigrate tracker 0001` reveals the exact raw SQL before it ever touches the database.
- **Database Safety:** `db.sqlite3` is safely ignored in `.gitignore` so test data and passwords are never pushed to GitHub.

### Block 4: ORM CRUD, Filters, Q Objects & Performance
- **Day 2 Exercise Query:** Querying across relationships using double underscores `__`:
  ```python
  Assignment.objects.filter(employee__department__code="ENG", status="ACTIVE")
  ```
- **`Q` Objects for OR Logic:**
  ```python
  Assignment.objects.filter(Q(status="COMPLETED") | Q(hours__gte=20.0))
  ```
- **The N+1 Query Problem & `select_related`:**
  - Without `select_related`: Accessing `assignment.employee.name` in a loop triggers 1 query + N additional employee queries.
  - With `select_related('employee__department')`: Performs a single **SQL `INNER JOIN`**, fetching assignments, employees, and departments in **1 database query**!
- **`prefetch_related`:** Used for reverse one-to-many relationships (`Department -> Employees`) in exactly 2 queries.

### Block 5: Django Admin Portal & Verification
- **Admin Registration (`tracker/admin.py`):** Configured `list_display`, `list_filter`, and `search_fields` for `Department`, `Employee`, and `Assignment`.
- **Interactive UI:** Non-technical managers can filter assignments by department or status directly in the browser at `/admin/`.

---

## 3. How to Demonstrate Live (Terminal Commands)

### A. Run the Day 2 ORM & SQL Inspection Demo:
```powershell
python query_workload.py
```
*(Prints active assignments, shows the generated raw SQL JOIN query, demonstrates `Q` filters, and verifies `select_related`).*

### B. Run the Django Automated Test Suite:
```powershell
python manage.py test
```
*(Runs 4 automated tests verifying model relationships, status filtering, and the API health check view).*

### C. Run the Local Development Server:
```powershell
python manage.py runserver
```
- Open health check: `http://127.0.0.1:8000/api/health/`
- Open Admin portal: `http://127.0.0.1:8000/admin/`

---

## 4. Common Questions & Answers for Your Demo

**Q: What is the difference between `makemigrations` and `migrate`?**  
*A: `makemigrations` reads your `models.py` and creates a version-controlled migration blueprint file. `migrate` executes that blueprint to actually create or modify tables in the database.*

**Q: What is the N+1 problem and how did you solve it?**  
*A: If you query N assignments and access their related employee, Django executes 1 query for assignments plus N queries for each employee (N+1 total). I solved this using `select_related('employee__department')`, which forces Django to perform an SQL `INNER JOIN` in a single query.*

**Q: When should you use `select_related` vs `prefetch_related`?**  
*A: Use `select_related` for single-object lookups (ForeignKeys and OneToOne) via SQL JOIN. Use `prefetch_related` for multi-object lookups (ManyToMany or reverse ForeignKeys like all employees in a department) via separate queries joined in memory.*

**Q: Why do we use `Q` objects?**  
*A: Standard `.filter()` calls always chain with SQL `AND`. To write complex `OR` conditions or `NOT` conditions, Django requires `Q` objects.*
