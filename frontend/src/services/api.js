/**
 * API Service for Workload Tracker
 * Handles communication with Django REST Framework backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

/**
 * Predefined tokens for demo users
 */
export const DEMO_USERS = [
  {
    id: 'alice_eng',
    name: 'Alice Chen',
    department: 'ENG',
    role: 'Engineer',
    token: '1ffa4be4a5dcedff4c91487e58e441636f3b897d',
  },
  {
    id: 'charlie_pm',
    name: 'Charlie Kim',
    department: 'PM',
    role: 'Product Manager',
    token: '903bed4b81f8ab2914117e26b076ad7336f49164',
  },
  {
    id: 'admin_lead',
    name: 'Admin Lead',
    department: 'ALL',
    role: 'Tech Lead / Staff',
    token: '29c91e52ac42992503bfa5ef3be0fe50b98b6e48',
  },
  {
    id: 'unauthenticated',
    name: 'Guest (No Auth Token)',
    department: 'None',
    role: 'Anonymous',
    token: null,
  },
];

/**
 * Builds request headers with Token authentication if provided.
 */
function getHeaders(token) {
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }
  return headers;
}

/**
 * Fetches assignments with optional department and status filters.
 */
export async function getAssignments(department = null, status = null, token = null, onTrace = null) {
  const params = new URLSearchParams();
  if (department && department !== 'ALL') {
    params.append('department', department);
  }
  if (status && status !== 'ALL') {
    params.append('status', status);
  }

  const queryString = params.toString() ? `?${params.toString()}` : '';
  const url = `${API_BASE_URL}/assignments/${queryString}`;

  const startTime = performance.now();
  const headers = getHeaders(token);

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers,
    });
    const latency = Math.round(performance.now() - startTime);
    const data = await response.json();

    if (onTrace) {
      onTrace({
        timestamp: new Date().toLocaleTimeString(),
        method: 'GET',
        url,
        status: response.status,
        statusText: response.statusText,
        latency: `${latency}ms`,
        headers,
        ok: response.ok,
      });
    }

    if (!response.ok) {
      const errorMsg = data.detail || (data.hours ? data.hours[0] : `HTTP Error ${response.status}: ${response.statusText}`);
      const err = new Error(errorMsg);
      err.status = response.status;
      err.data = data;
      throw err;
    }

    return data.results ? data.results : data;
  } catch (err) {
    if (onTrace && !err.status) {
      onTrace({
        timestamp: new Date().toLocaleTimeString(),
        method: 'GET',
        url,
        status: 0,
        statusText: 'Network / Connection Error',
        latency: `${Math.round(performance.now() - startTime)}ms`,
        headers,
        ok: false,
      });
    }
    throw err;
  }
}

/**
 * Fetches all employees for selection in assignment creation.
 */
export async function getEmployees(token = null) {
  const url = `${API_BASE_URL}/employees/`;
  const response = await fetch(url, {
    method: 'GET',
    headers: getHeaders(token),
  });

  if (!response.ok) {
    return [];
  }
  const data = await response.json();
  return data.results ? data.results : data;
}

/**
 * Fetches department workload summary metrics.
 */
export async function getDepartmentSummary(department = null, token = null) {
  let url = `${API_BASE_URL}/assignments/summary/`;
  if (department && department !== 'ALL') {
    url += `?department=${encodeURIComponent(department)}`;
  }

  const response = await fetch(url, {
    method: 'GET',
    headers: getHeaders(token),
  });

  if (!response.ok) {
    return null;
  }
  return await response.json();
}

/**
 * Creates a new assignment (POST /api/assignments/).
 * Enforces cross-department permissions on backend.
 */
export async function createAssignment(assignmentData, token = null, onTrace = null) {
  const url = `${API_BASE_URL}/assignments/`;
  const startTime = performance.now();
  const headers = getHeaders(token);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(assignmentData),
    });
    const latency = Math.round(performance.now() - startTime);
    const data = await response.json();

    if (onTrace) {
      onTrace({
        timestamp: new Date().toLocaleTimeString(),
        method: 'POST',
        url,
        status: response.status,
        statusText: response.statusText,
        latency: `${latency}ms`,
        headers,
        payload: assignmentData,
        ok: response.ok,
      });
    }

    if (!response.ok) {
      let errorMsg = data.detail;
      if (!errorMsg && typeof data === 'object') {
        const firstKey = Object.keys(data)[0];
        errorMsg = `${firstKey}: ${Array.isArray(data[firstKey]) ? data[firstKey][0] : data[firstKey]}`;
      }
      const err = new Error(errorMsg || `Error ${response.status}: ${response.statusText}`);
      err.status = response.status;
      err.data = data;
      throw err;
    }

    return data;
  } catch (err) {
    throw err;
  }
}

/**
 * Partially updates an assignment (hours and/or status).
 */
export async function updateAssignment(id, updateData, token = null, onTrace = null) {
  const url = `${API_BASE_URL}/assignments/${id}/`;
  const startTime = performance.now();
  const headers = getHeaders(token);

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(updateData),
    });
    const latency = Math.round(performance.now() - startTime);
    const data = await response.json();

    if (onTrace) {
      onTrace({
        timestamp: new Date().toLocaleTimeString(),
        method: 'PATCH',
        url,
        status: response.status,
        statusText: response.statusText,
        latency: `${latency}ms`,
        headers,
        payload: updateData,
        ok: response.ok,
      });
    }

    if (!response.ok) {
      const errorMsg = data.detail || (data.hours ? data.hours[0] : `Error ${response.status}: ${response.statusText}`);
      const err = new Error(errorMsg);
      err.status = response.status;
      err.data = data;
      throw err;
    }

    return data;
  } catch (err) {
    throw err;
  }
}
