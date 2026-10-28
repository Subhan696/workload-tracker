# Pull Request: Full-Stack Workload Tracker Capstone Implementation

## 🎯 Description & Summary
This pull request delivers the complete **Day 5 Full-Stack Capstone Feature** for the Workload Tracker training program. It connects the React.js SPA frontend to the Django REST Framework backend, providing end-to-end assignment management, dynamic workload aggregation, combined department and status filtering, and strict object-level permission enforcement.

---

## 🏗️ Architecture & Data-Flow Changes

### 1. Frontend (React 18 + Vite)
- **Controlled Creation Form (`CreateAssignmentModal.jsx`)**: Enables adding new assignments with dynamic employee selection and client-side hours validation (`0.5 <= h <= 168`).
- **Inline Status & Hours Editor (`AssignmentCard.jsx`)**: Supports updating assignment status (`ACTIVE`, `ON_HOLD`, `COMPLETED`) and allocated hours via authenticated `PATCH` requests.
- **Combined Department & Status Filter (`DepartmentFilter.jsx`)**: Enables multi-parameter query filtering (`/api/assignments/?department=...&status=...`).
- **Live Traceability Inspector (`NetworkInspector.jsx`)**: Captures all HTTP operations, latency, and status codes for transparent debugging and evaluation.
- **Minimal Monochrome Design (`index.css` & `App.css`)**: High-contrast, clean black & white design system free of extraneous visual artifacts.

### 2. Backend (Django 5.x & Django REST Framework)
- **Object-Level Permissions (`tracker/permissions.py`)**: `IsSameDepartmentOrReadOnly` restricts cross-department edits (`403 Forbidden`).
- **Cross-Department Creation Guard (`tracker/views.py`)**: `perform_create()` prevents non-staff users from creating assignments for employees in other departments.
- **Serializer Field Validation (`tracker/serializers.py`)**: `validate_hours()` rejects negative hours and hours exceeding 168h/week.
- **N+1 Query Elimination (`tracker/views.py`)**: Uses `select_related('employee__department')` for single-query retrieval across foreign key relationships.
- **CORS Configuration (`config/settings.py`)**: `django-cors-headers` middleware configured for Vite dev server.

---

## 🧪 Test Evidence

### 1. Automated Full-Stack End-to-End Tests (`python demo_day5_fullstack.py`)
```text
========================================================================
  DAY 5: FULL-STACK CAPSTONE END-TO-END VERIFICATION
========================================================================

[Test 1: Combined Filter (?department=ENG&status=ACTIVE)]
   GET /api/assignments/?department=ENG&status=ACTIVE -> Status: 200 OK
   Active ENG Assignments Count: 7

[Test 2: Cross-Department Creation Rejection (Alice [ENG] -> Charlie [PM])]
   POST /api/assignments/ (Cross-Dept) -> Status: 403 (Expected: 403 Forbidden)
   Response Detail: Cannot create assignments for other departments.

[Test 3: Same-Department Creation (Alice [ENG] -> Bob [ENG])]
   POST /api/assignments/ -> Status: 201 (Expected: 201 Created)
   Created Assignment: ID #12 - 'Day 5 Capstone Verification Task' (18.0h)

[Test 4: Input Validation (Hours = -10.0)]
   POST /api/assignments/ (hours: -10) -> Status: 400 (Expected: 400 Bad Request)
   Validation Error: {'hours': [ErrorDetail(string='Hours cannot be negative.', code='invalid')]}

[Test 5: Full Data-Flow Update (PATCH /api/assignments/12/)]
   PATCH /api/assignments/12/ -> Status: 200 OK
   Updated Status: COMPLETED, Updated Hours: 20.0h

[Test 6: Department Workload Summary Aggregation]
   GET /api/assignments/summary/?department=ENG -> Status: 200 OK
   Aggregated Metrics: {'department': 'ENG', 'total_assignments': 9, 'active_allocated_hours': 144.0, 'total_allocated_hours': 174.0}

[Test 7: Staff/Admin Cross-Department Override]
   POST /api/assignments/ by Admin -> Status: 201 (Expected: 201 Created)

========================================================================
  ALL 7 DAY 5 FULL-STACK CAPSTONE TESTS PASSED SUCCESSFULLY!
========================================================================
```

### 2. Django Unit Test Suite (`python manage.py test`)
```text
Ran 12 tests in 10.589s

OK
Destroying test database for alias 'default'...
```

---

## 📋 Review Checklist
- [x] Branch branched from clean upstream (`feature/day4-react-frontend`).
- [x] Code adheres to repository style standards (monochrome minimal design, no unapproved libraries).
- [x] Zero hardcoded secrets or environment variables (`.env` properly ignored).
- [x] Automated test coverage covers all happy paths and security edge cases (401, 403, 400, 201, 200).
- [x] Documentation complete with live 5-minute evaluation guide (`DAY5_EXPLANATION.md`).
