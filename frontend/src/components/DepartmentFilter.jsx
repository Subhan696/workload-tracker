import React from 'react';

const DEPARTMENTS = [
  { code: 'ALL', label: 'All' },
  { code: 'ENG', label: 'Engineering' },
  { code: 'PM', label: 'Product Management' },
  { code: 'QA', label: 'Quality Assurance' },
];

const STATUSES = ['ALL', 'ACTIVE', 'ON_HOLD', 'COMPLETED'];

export default function DepartmentFilter({
  selectedDept,
  onSelectDept,
  selectedStatus,
  onSelectStatus,
  onOpenCreate,
  onRefresh,
  loading,
}) {
  return (
    <div className="filter-toolbar" id="filter-toolbar">
      <div className="filter-group" id="dept-pills-group">
        <span className="filter-label">Dept:</span>
        {DEPARTMENTS.map((dept) => {
          const isActive = selectedDept === dept.code;
          return (
            <button
              key={dept.code}
              id={`filter-dept-${dept.code.toLowerCase()}`}
              className={`dept-pill ${isActive ? 'active' : ''}`}
              onClick={() => onSelectDept(dept.code)}
            >
              {dept.label} ({dept.code})
            </button>
          );
        })}

        <span className="filter-label" style={{ marginLeft: '12px' }}>Status:</span>
        <select
          id="filter-status-select"
          value={selectedStatus}
          onChange={(e) => onSelectStatus(e.target.value)}
          style={{ fontSize: '12px', padding: '4px 8px' }}
        >
          {STATUSES.map((stat) => (
            <option key={stat} value={stat}>
              {stat === 'ALL' ? 'All Statuses' : stat}
            </option>
          ))}
        </select>
      </div>

      <div className="action-buttons">
        <button
          id="btn-open-create"
          className="btn-primary"
          onClick={onOpenCreate}
          style={{ background: '#ffffff', color: '#000000', borderColor: '#ffffff', fontWeight: 600 }}
        >
          + Add Assignment
        </button>
        <button
          id="btn-refresh-assignments"
          onClick={onRefresh}
          disabled={loading}
        >
          {loading ? 'Fetching...' : 'Refresh'}
        </button>
      </div>
    </div>
  );
}
