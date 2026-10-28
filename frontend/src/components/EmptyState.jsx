import React from 'react';

export default function EmptyState({ department, onResetFilter }) {
  return (
    <div className="empty-state" id="empty-state-view">
      <h3>No Assignments Found</h3>
      <p>
        No assignments match filter:{' '}
        <strong>{department === 'ALL' ? 'All Departments' : department}</strong>.
      </p>
      {department !== 'ALL' && (
        <button
          id="btn-reset-filter"
          onClick={onResetFilter}
        >
          View All Departments
        </button>
      )}
    </div>
  );
}
