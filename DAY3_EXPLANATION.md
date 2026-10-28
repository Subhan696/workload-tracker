# Day 3: Django REST Framework (DRF) APIs & 5-Minute Demo Guide

This document is your complete walkthrough to explain **Day 3** to your mentor, team lead, or evaluator.

---

## 1. High-Level Summary (The 30-Second Elevator Pitch)
> "In Day 3, we built enterprise-grade RESTful APIs using Django REST Framework (DRF). We converted our database models into JSON using Serializers with field-level validations, configured ViewSets with clean DefaultRouter URL routing, enforced authentication and department-level permissions, implemented query filtering and pagination, and proved API robustness by verifying 401 Unauthorized, 400 Bad Request on invalid hours, 200/201 on success, and 403 Forbidden on unauthorized cross-department edits."

---

## 2. Walkthrough of the 5 Core Blocks

### Block 1: HTTP, REST & Status Codes
- **REST Principles:** Resources are exposed via nouns (`/api/assignments/`) and acted upon using standard HTTP verbs:
  - `GET`: Read data (Status: `200 OK`).
  - `POST`: Create a new assignment (Status: `201 Created`).
  - `PATCH`: Partially update an assignment (Status: `200 OK`).
  - `DELETE`: Remove an assignment (Status: `204 No Content`).
- **HTTP Error Codes:**
  - `401 Unauthorized`: Client provided no or invalid authentication credentials.
  - `403 Forbidden`: Client is authenticated, but not permitted to access/modify this resource (e.g. cross-department access).
  - `400 Bad Request`: Validation failure (e.g., negative hours).
  - `404 Not Found`: Requested resource ID does not exist.

### Block 2: Serializers, ViewSets & Routers
- **ModelSerializers (`tracker/serializers.py`):** Converts complex Django model instances into Python native data types that easily render into JSON, and parses incoming JSON back into validated model instances.
- **`AssignmentSerializer`:**
  - Includes convenience read-only fields: `employee_name`, `department_code`, and `department_name`.
  - Implements field-level validation:
    ```python
    def validate_hours(self, value):
        if value < 0:
            raise serializers.ValidationError("Hours cannot be negative.")
        if value > 168:
            raise serializers.ValidationError("Hours cannot exceed 168 hours in a single week.")
        return round(float(value), 2)
    ```
- **`AssignmentViewSet` (`tracker/views.py`):** Combines logic for `list`, `retrieve`, `create`, `partial_update`, and `destroy` into a single class.
- **`DefaultRouter` (`tracker/urls.py`):** Automatically generates the full RESTful routing tree (`/api/assignments/`, `/api/assignments/<id>/`) without manual regex path writing.

### Block 3: Authentication & Department Permissions
- **Authentication:** Configured `BasicAuthentication`, `TokenAuthentication`, and `SessionAuthentication` in `settings.py`.
- **Custom Permission (`IsSameDepartmentOrReadOnly`):**
  - Read actions (`GET`) are permitted to all authenticated users.
  - Edit/Delete actions (`PATCH`, `DELETE`) are restricted:
    - Staff / Admins can edit any department.
    - Regular employees can **only** edit assignments within their own department.
    - If a Product Manager attempts to edit an Engineering assignment, DRF immediately blocks it with **`403 Forbidden`**.

### Block 4: Filtering, Pagination & Validation
- **Query Parameter Filtering:** Overrode `get_queryset()` to support filtering:
  - `GET /api/assignments/?department=ENG` (filters by department code)
  - `GET /api/assignments/?status=ACTIVE` (filters by active status)
- **Pagination:** Global `PageNumberPagination` configured in `settings.py` with `PAGE_SIZE = 10`.

### Block 5: Automated API Tests (Test Evidence)
- Automated test suite in `tracker/test_api.py` (8 API tests + 4 model tests = **12 tests passing**).
- Verified:
  1. `401 Unauthorized` for unauthenticated requests.
  2. `200 OK` for authenticated `GET`.
  3. `201 Created` for valid `POST`.
  4. `400 Bad Request` for negative hours (`-15.0h`).
  5. `200 OK` for valid `PATCH`.
  6. `403 Forbidden` for cross-department edits.

---

## 3. How to Demonstrate Live (Terminal Commands)

### A. Run the Day 3 Live API Demonstration:
```powershell
python demo_day3_api.py
```
*(Executes unauthenticated check, authenticated GET, department filter, 400 Bad Request validation, 201 Created POST, 200 OK PATCH, and 403 Forbidden cross-department block).*

### B. Run the Automated Test Suite:
```powershell
python manage.py test
```
**Result:** `Ran 12 tests -> OK` (100% test pass)

### C. Test in Browser (Browsable API):
```powershell
python manage.py runserver
```
- Open `http://127.0.0.1:8000/api/assignments/`
- Open `http://127.0.0.1:8000/api/assignments/?department=ENG`
- Open summary endpoint: `http://127.0.0.1:8000/api/assignments/summary/?department=ENG`

---

## 4. Common Questions & Answers for Your Demo

**Q: What is the primary role of a DRF Serializer?**  
*A: Serializers act as the bidirectional bridge between Django ORM models and JSON. They serialize database queries into JSON responses and deserialize/validate incoming JSON payloads into model instances.*

**Q: What is the difference between 401 Unauthorized and 403 Forbidden?**  
*A: `401 Unauthorized` means "Who are you?" (authentication credentials missing or invalid). `403 Forbidden` means "I know who you are, but you do not have permission to perform this action" (e.g. cross-department unauthorized edit).*

**Q: How does `DefaultRouter` help compared to manual `path()` definitions?**  
*A: `DefaultRouter` automatically binds standard REST conventions (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`) to their corresponding HTTP methods and URL patterns, eliminating boilerplate code.*

**Q: How did you implement object-level permissions?**  
*A: By creating `IsSameDepartmentOrReadOnly(BasePermission)` and implementing `has_object_permission()`. It checks if `request.user.employee_profile.department` matches the assignment's department before allowing `PATCH` or `DELETE`.*
