# Day 4: React.js & Full-Stack Integration (5-Minute Demo Guide)

This document is your complete walkthrough to explain and demonstrate **Day 4** to your mentor, team lead, or evaluator.

---

## 1. High-Level Summary (The 30-Second Elevator Pitch)

> "In Day 4, we built a modern React.js frontend application that seamlessly integrates with our Day 3 Django REST Framework backend. We established a clean component hierarchy with reusable UI elements, leveraged `useState` and `useEffect` for reactive state management, implemented department filtering, controlled forms with input validation, handled all asynchronous UI states (loading skeleton, empty state, and 403/401 error alerts), and built a live Full-Stack Network Inspector demonstrating complete request-to-UI traceability."

---

## 2. Walkthrough of the 5 Core Blocks

### Block 1: React Structure, JSX, Components, Props & Reusable UI
- **Project Structure:** Scaffolded with Vite in `frontend/`:
  - `src/components/Header.jsx`: Top navigation with brand identity, live API health indicator, and interactive active-user switcher.
  - `src/components/SummaryStats.jsx`: KPI cards showing total assignments, active workload hours, and total allocated hours.
  - `src/components/DepartmentFilter.jsx`: Reusable department filter toolbar with pill buttons (`ALL`, `ENG`, `PM`, `QA`).
  - `src/components/AssignmentCard.jsx`: Reusable card component displaying assignment title, employee details, department tag, status, hours, and inline editing.
  - `src/components/LoadingState.jsx`: Clean minimal loading indicator.
  - `src/components/EmptyState.jsx`: Clean, user-friendly empty state when zero assignments match a filter.
  - `src/components/ErrorState.jsx`: Actionable alert banner with status codes and a retry button.
  - `src/components/NetworkInspector.jsx`: Traceability drawer logging HTTP method, endpoint, latency, and status code.
- **Props Flow:** Unidirectional data flow from `App.jsx` down to children components, ensuring isolation and clean separation of concerns.

---

### Block 2: `useState`, `useEffect`, Events & Conditional Rendering
- **`useState` Hooks:**
  - `assignments`: Current list of assignments loaded from the backend.
  - `selectedDept`: Active filter ('ALL', 'ENG', 'PM', 'QA').
  - `loading`: Boolean state controlling the skeleton loading view.
  - `error`: Stores API failure exceptions (e.g. 403 Forbidden or network loss).
  - `currentUser`: Active authentication profile (Alice Chen, Charlie Kim, Admin Lead, or Guest).
  - `networkTraces`: Array of recent HTTP network operations for live inspection.
- **`useEffect` Hook:**
  - Triggers automated data fetching whenever `selectedDept` or `currentUser` changes.
- **Conditional Rendering Hierarchy:**
  ```jsx
  {loading ? (
    <LoadingState />
  ) : error ? (
    <ErrorState error={error} onRetry={loadData} currentUser={currentUser} />
  ) : assignments.length === 0 ? (
    <EmptyState department={selectedDept} onResetFilter={() => setSelectedDept('ALL')} />
  ) : (
    <div className="assignment-grid">
      {assignments.map(assignment => (
        <AssignmentCard key={assignment.id} assignment={assignment} onUpdateHours={handleUpdateHours} />
      ))}
    </div>
  )}
  ```

---

### Block 3: Controlled Forms, Validation & List Rendering
- **Controlled Input:**
  - The `AssignmentCard` contains an inline hours editor (`useState(hoursInput)`).
- **Client-Side Validation:**
  - Replicates backend business rules before network transmission:
    - Rejects negative hours (`hours < 0`).
    - Rejects hours exceeding weekly limit (`hours > 168`).
    - Disables action buttons during network transit to prevent duplicate submissions.
- **Keyed List Rendering:**
  - Every assignment element is rendered using `assignment.id` as a stable key, ensuring optimal React Virtual DOM reconciliation.

---

### Block 4: API Calls, Async/Await & Full-Stack Integration
- **API Service Layer (`src/services/api.js`):**
  - Uses `async/await` and native browser `fetch()`:
    - `getAssignments(department, token)`: Appends query parameter `?department=<code` and injects `Authorization: Token <key>`.
    - `getDepartmentSummary(department, token)`: Fetches aggregate metrics from `/api/assignments/summary/`.
    - `updateAssignmentHours(id, hours, token)`: Sends `PATCH /api/assignments/<id>/` with updated hours payload.
- **CORS & Dev Server Proxy:**
  - Django configured with `django-cors-headers` (`CORS_ALLOWED_ORIGINS = ['http://localhost:5173']`).
  - Vite dev server configured with `/api` proxy directly to `http://127.0.0.1:8000`, eliminating cross-origin hurdles during local development.

---

### Block 5: React DevTools, Browser Debugging & Git Collaboration
- **Browser Network Debugging:**
  - Inspecting Network tab in Chrome DevTools reveals headers, payload, response JSON, and timing metrics.
- **Live Traceability Inspector:**
  - The embedded inspector on the dashboard displays the exact HTTP method (`GET`, `PATCH`), endpoint, latency, and status (`200 OK`, `403 Forbidden`).
- **Git Collaboration Fundamentals:**
  - `git fetch origin`: Downloads remote commits and branches without altering the working tree.
  - `git pull --ff-only`: Fast-forwards current branch only if no local diversion exists, preventing accidental merge commits.
  - **Merge vs. Rebase:**
    - *Merge*: Creates a two-parent merge commit preserving true chronological history.
    - *Rebase*: Re-applies local commits on top of upstream, producing a clean, linear commit history.
  - **Conflict Resolution:** Inspect conflicting blocks (`<<<<<<< HEAD`, `=======`, `>>>>>>>`), choose correct code, test locally, stage with `git add`, and finalize commit.

---

## 3. How to Demonstrate Live (5-Minute Demo Script)

### Step 1: Start the Full-Stack Environment
Ensure both backend and frontend servers are running:
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

1. **Show Initial State & Component Structure (30 seconds):**
   - *"Here is the Workload Tracker React application. In the top navigation, you can see our live backend connection indicator and user switcher. Below are the KPI cards computing total assignments and allocated hours in real time."*

2. **Demonstrate Department Filtering (1 minute):**
   - Click **'Engineering (ENG)'**:
     - *"When I click Engineering, React updates the `selectedDept` state. The `useEffect` triggers a GET request to `/api/assignments/?department=ENG`, and the UI dynamically re-renders only Engineering assignments."*
   - Click **'Product Management (PM)'**:
     - *"Similarly, filtering by PM instantly updates the view and the workload KPIs."*
   - Click **'All Departments (ALL)'** to reset.

3. **Demonstrate Controlled Form & Hours Update (1.5 minutes):**
   - On the first card, click **'✏️ Edit Hours'**.
   - Enter `-5` and click Save:
     - *"Notice client-side validation catches this immediately with 'Hours cannot be negative', preventing an unnecessary network call."*
   - Change hours to a valid number (e.g. `28.0`) and click Save:
     - *"Now React sends an authenticated `PATCH /api/assignments/1/` request. The backend validates and updates the database, returning `200 OK`, and React smoothly updates the card and the summary stats."*

4. **Demonstrate Authentication & Error State (1 minute):**
   - In the top-right user switcher, select **'Guest (No Auth Token)'**:
     - *"When unauthenticated, the backend rejects the request with `403 Forbidden`. Notice how React transitions into a dedicated Error State view with an error banner and a 'Retry API Request' button."*
   - Switch back to **'Alice Chen (ENG)'** to restore access.

5. **Show Request-to-UI Traceability (1 minute):**
   - Scroll down to the **'Full-Stack Network & State Inspector'**:
     - *"Here in our inspector drawer, we can trace every single React user interaction through its corresponding HTTP request, response code, and latency, proving complete end-to-end fullstack integration."*

---

## 4. Evaluator Q&A Preparation

**Q: Why do we use `useEffect` for data fetching instead of calling the API directly inside the component body?**  
*A: Calling an API directly inside the component body would trigger on every single render cycle, causing an infinite loop of fetches and re-renders. `useEffect` lets us declare explicit dependency arrays (`[selectedDept, currentUser]`), ensuring API calls run only on mount or when specific state values change.*

**Q: What is the benefit of configuring a proxy in `vite.config.js`?**  
*A: The proxy routes frontend requests (e.g. `/api/...`) to `http://127.0.0.1:8000` behind the scenes. This eliminates CORS configuration issues in development and allows identical relative API URLs across development and production.*

**Q: How does React handle conditional rendering safely?**  
*A: We use ternary operators and short-circuit evaluation (`condition ? <Component /> : null`) to render states hierarchically: loading skeleton first, error state second, empty state third, and data cards fourth.*

**Q: When would you choose `git pull --ff-only` over a regular `git pull`?**  
*A: `git pull --ff-only` ensures you only pull if your local branch can be fast-forwarded without creating an unexpected merge commit. If branches have diverged, it halts safely, allowing you to review changes or rebase intentionally.*
