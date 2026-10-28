import React from 'react';

const DEPARTMENTS = [
  { code: 'ALL', label: 'All' },
  { code: 'ENG', label: 'Engineering' },
  { code: 'PM', label: 'Product Management' },
  { code: 'QA', label: 'Quality Assurance' },
];

export default function DepartmentFilter({ selectedDept, onSelectDept, onRefresh, loading }) {
  return (
    <div className="filter-toolbar" id="filter-toolbar">
      <div className="filter-group" id="dept-pills-group">
        <span className="filter-label">Department:</span>
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
      </div>

      <div className="action-buttons">
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
