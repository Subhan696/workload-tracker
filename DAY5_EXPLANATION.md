# Day 5: Full-Stack Capstone, Data-Flow Traceability & Final Evaluation Guide

This document is your complete walkthrough to explain and demonstrate **Day 5** to your mentor, team lead, or evaluator.

---

## 1. High-Level Summary (The 30-Second Elevator Pitch)

> "In Day 5, we brought together the entire 5-day curriculum into an enterprise full-stack feature. We built the complete end-to-end Assignment Management & Workload Allocation flow: combined department and status filtering, controlled assignment creation with client and backend validation, status transitions, and object-level permission enforcement. Most importantly, we can trace a user action seamlessly across all 7 layers of the stack: from the React UI and async fetch service, through the Django URL router, ViewSet, and permissions layer, down through DRF serializer validation, into the ORM, and finally persisting into SQLite."

---

## 2. Complete End-to-End Data Flow Trace (The 7 Layers)

Here is how data flows from the user's click in the browser down to the disk database:

```
[1. User Interaction]   User fills "+ Add Assignment" form & clicks Submit
         │
         ▼
[2. React State (UI)]   CreateAssignmentModal validates hours (0.5 <= h <= 168)
         │              Triggers handleCreateAssignment() in App.jsx
         ▼
[3. HTTP Service]       api.js issues: POST /api/assignments/
         │              Headers: { 'Authorization': 'Token 1ffa4be...', 'Content-Type': 'application/json' }
         │              Body: { title: "...", employee: 2, hours: 18.0, status: "ACTIVE" }
         ▼
[4. URL Router]         config/urls.py -> tracker/urls.py -> DefaultRouter
         │              Routes POST /api/assignments/ -> AssignmentViewSet.create()
         ▼
[5. Auth & Permissions] TokenAuthentication resolves user (Alice Chen, ENG)
         │              AssignmentViewSet.perform_create checks if user.department == employee.department
         │              If mismatch: raises PermissionDenied (HTTP 403 Forbidden)
         ▼
[6. Serializer Validate] AssignmentSerializer runs field validation:
         │              - validate_hours(value): rejects < 0 or > 168
         │              - employee existence & status choice validation
         ▼
[7. Django ORM & DB]    serializer.save() executes:
                        INSERT INTO tracker_assignment (title, employee_id, hours, status)
                        VALUES ('...', 2, 18.0, 'ACTIVE');
         │              Persisted in db.sqlite3
         ▼
[8. Return & Re-render] Backend responds with HTTP 201 Created & serialized JSON
                        React adds trace to Network Inspector, updates state, and re-renders UI!
```

---

## 3. Walkthrough of the 5 Core Blocks

### Block 1: Architecture Walkthrough
- **Decoupled Architecture:**
  - Backend: Django 5.x + Django REST Framework exposing clean RESTful JSON endpoints (`/api/assignments/`, `/api/departments/`, `/api/employees/`, `/api/assignments/summary/`).
  - Frontend: React 18 + Vite running as an independent SPA with a proxy bridge eliminating CORS during local development.
- **Relational Integrity:**
  - `Department` 1 &rarr; N `Employee` 1 &rarr; N `Assignment`.
  - Every assignment tracks hours, status (`ACTIVE`, `ON_HOLD`, `COMPLETED`), and foreign key relationships.

---

### Block 2: Data Flow Traceability
- **Request Tracing:**
  - Every request is logged in the embedded **Network & Request Inspector** on the dashboard.
  - Demonstrates latency, HTTP method, URL query parameters (`?department=ENG&status=ACTIVE`), and status codes (`200 OK`, `201 Created`, `403 Forbidden`).

---

### Block 3: The Capstone Assignment Feature
- **Department & Status Filtering Synergy:**
  - Users can filter by Department (`ALL`, `ENG`, `PM`, `QA`) and Status (`ALL`, `ACTIVE`, `ON_HOLD`, `COMPLETED`) simultaneously.
  - Workload metrics dynamically re-aggregate active vs total hours.
- **Assignment Creation Modal (`+ Add Assignment`):**
  - Controlled inputs for Title, Employee dropdown, Hours, and Status.
  - Client-side validation catches empty titles and negative hours immediately.
- **Inline Status & Hours Update:**
  - Assignments can be updated inline (e.g. marking a task `COMPLETED` or adjusting hours), triggering immediate `PATCH` updates.

---

### Block 4: Permissions & Edge Case Verification
- **Cross-Department Permission Guard:**
  - Regular employees (e.g., Alice Chen in ENG) can only create or edit assignments for their own department.
  - Attempting to assign work to another department (e.g. Charlie Kim in PM) is rejected with **`403 Forbidden: Cannot create assignments for other departments.`**
- **Admin Superuser Override:**
  - Staff / Admins (`admin_lead`) have global administrative privileges to assign and edit work across any department.
- **Negative & Excessive Hours Guard:**
  - Validated on both client and backend: `hours < 0` or `hours > 168` is rejected with **`400 Bad Request`**.

---

### Block 5: Git PR Workflow & Review Checklist
- **Branch Strategy:**
  - Main branch (`main`) is protected.
  - Short-lived feature branches:
    - `feature/day1-python-workload`
    - `feature/day2-django-setup`
    - `feature/day3-drf-apis`
    - `feature/day4-react-frontend`
    - `feature/day5-fullstack-capstone`
- **Review Hygiene Checklist:**
  1. Base branch confirmed (`main`).
  2. Git diff inspected (`git diff`).
  3. Automated unit tests passing (`python manage.py test` -> 12 tests OK).
  4. End-to-end fullstack tests passing (`python demo_day5_fullstack.py` -> 7 tests OK).
  5. Zero secrets or API keys committed (`.env` ignored in `.gitignore`).

---

## 4. How to Demonstrate Live (5-Minute Evaluation Script)

### Step 1: Ensure Servers Are Running
```powershell
# Terminal 1: Django Backend
python manage.py runserver

# Terminal 2: React Frontend
cd frontend
npm run dev
```
Open **`http://localhost:5173/`** in your browser.

---

### Step 2: Live Demo Script (What to Say & Do)

1. **Introduction & Architecture (45 seconds):**
   - *"Welcome! Today I will demonstrate our completed full-stack Workload Tracker application. We have built an end-to-end system where a React SPA communicates with a Django REST Framework backend over authenticated REST APIs, backed by SQLite with strict relational integrity and role-based permissions."*

2. **Demonstrate Combined Department & Status Filtering (1 minute):**
   - Click **'Engineering (ENG)'** in the Dept filter toolbar.
   - Select **'ACTIVE'** from the Status dropdown.
   - *"Notice how the list immediately filters to only Active Engineering assignments, and the KPI cards recompute active allocated hours in real time."*

3. **Demonstrate Assignment Creation & Cross-Department Security (1.5 minutes):**
   - In the top-right User switcher, verify you are logged in as **`Alice Chen (ENG)`**.
   - Click **`+ Add Assignment`**.
   - **Test Unauthorized Cross-Dept Creation:**
     - Title: `Mobile Roadmap Alignment`
     - Employee: Select `Charlie Kim (PM)`
     - Hours: `15.0`
     - Click **Create Assignment**:
     - *"Notice the backend rejects this with 'Cannot create assignments for other departments.' This proves our backend object-level permissions cannot be bypassed from the client."*
   - **Test Valid Same-Dept Creation:**
     - Change Employee to `Bob Martinez (ENG)`.
     - Click **Create Assignment**:
     - *"The assignment is accepted (`201 Created`), the modal closes, the card appears in the list, and the total workload re-aggregates immediately."*

4. **Demonstrate Status & Hours Update (1 minute):**
   - On the new card, click **`Edit`**.
   - Change Status from `ACTIVE` to **`COMPLETED`** and click **Save**.
   - *"React issues an authenticated `PATCH /api/assignments/<id>/`. The status updates, and the Active Workload hours KPI decreases because the task is no longer in progress."*

5. **Show Traceability in Network Inspector (45 seconds):**
   - Scroll down to the **Network & Request Inspector** table:
     - *"Every action we just performed—the GET filter, the 403 rejected POST, the 201 successful POST, and the 200 PATCH update—is captured right here with latency and status codes, proving complete end-to-end traceability from the UI through to the database."*

---

## 5. Automated Verification Evidence

To prove system stability to your evaluator in the terminal, run:

```powershell
# 1. Run the End-to-End Capstone Test Script:
python demo_day5_fullstack.py

# 2. Run the Full Django Automated Unit Test Suite:
python manage.py test
```

**Results:**
- `demo_day5_fullstack.py`: 7/7 End-to-End Tests Passed.
- `python manage.py test`: 12/12 Unit Tests Passed (`OK`).

---

## 6. Evaluator Q&A Preparation

**Q: How does your system prevent a user from tampering with client-side JavaScript to assign work across departments?**  
*A: We adhere to the zero-trust principle: client-side validation is solely for user experience. In the backend `perform_create()` method of `AssignmentViewSet`, we inspect `request.user.employee_profile.department` against `employee.department`. If they do not match and the user is not staff, DRF aborts the request with a `403 Forbidden` exception before `serializer.save()` is ever reached.*

**Q: Can you trace what happens behind the scenes when a user clicks 'Edit' and changes the status to 'COMPLETED'?**  
*A: When the user saves, `AssignmentCard` calls `onUpdate()`, triggering `api.js` to dispatch an HTTP `PATCH /api/assignments/<id>/` with `{ status: 'COMPLETED' }`. Django's URL resolver routes this to `AssignmentViewSet.partial_update()`. DRF validates the status choice, executes an `UPDATE tracker_assignment SET status = 'COMPLETED' WHERE id = <id>`, and returns a `200 OK`. React receives the JSON, updates state via `setAssignments()`, and re-renders the card.*

**Q: How does the N+1 problem apply to this assignment listing endpoint, and how did you prevent it?**  
*A: An assignment references an employee, which in turn references a department. Without optimization, querying 10 assignments would trigger 1 query for assignments + 10 queries for employees + 10 queries for departments (21 queries). In `AssignmentViewSet`, we configured `queryset = Assignment.objects.select_related('employee__department').all()`, which joins all three tables in a single SQL query.*
