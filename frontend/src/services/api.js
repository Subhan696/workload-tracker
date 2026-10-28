/**
 * API Service for Workload Tracker
 * Handles communication with Django REST Framework backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

/**
 * Predefined tokens for Day 3 & 4 demo users
 */
export const DEMO_USERS = [
  {
    id: 'alice_eng',
    name: 'Alice Chen',
    department: 'ENG',
    role: 'Engineer',
    token: '1ffa4be4a5dcedff4c91487e58e441636f3b897d',
    color: '#3b82f6',
  },
  {
    id: 'charlie_pm',
    name: 'Charlie Kim',
    department: 'PM',
    role: 'Product Manager',
    token: '903bed4b81f8ab2914117e26b076ad7336f49164',
    color: '#8b5cf6',
  },
  {
    id: 'admin_lead',
    name: 'Admin Lead',
    department: 'ALL',
    role: 'Tech Lead / Staff',
    token: '29c91e52ac42992503bfa5ef3be0fe50b98b6e48',
    color: '#10b981',
  },
  {
    id: 'unauthenticated',
    name: 'Unauthenticated (Guest)',
    department: 'None',
    role: 'Guest / Anonymous',
    token: null,
    color: '#ef4444',
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
 * Fetches assignments with optional department filter.
 * Traces request details for Day 4 network debugging demonstration.
 */
export async function getAssignments(department = null, token = null, onTrace = null) {
  let url = `${API_BASE_URL}/assignments/`;
  if (department && department !== 'ALL') {
    url += `?department=${encodeURIComponent(department)}`;
  }

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

    // Handles both paginated { count, results: [] } and raw array responses
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
 * Partially updates an assignment (e.g. allocated hours).
 * Demonstrates PATCH request and permission checking.
 */
export async function updateAssignmentHours(id, hours, token = null, onTrace = null) {
  const url = `${API_BASE_URL}/assignments/${id}/`;
  const startTime = performance.now();
  const headers = getHeaders(token);
  const payload = { hours: parseFloat(hours) };

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(payload),
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
        payload,
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
