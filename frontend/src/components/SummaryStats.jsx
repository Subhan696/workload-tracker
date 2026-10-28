import React from 'react';

export default function SummaryStats({ assignments, summaryData }) {
  const totalCount = assignments.length;
  const activeHours = assignments
    .filter((a) => a.status === 'ACTIVE')
    .reduce((sum, a) => sum + parseFloat(a.hours || 0), 0);
  const totalHours = assignments.reduce((sum, a) => sum + parseFloat(a.hours || 0), 0);

  const displayActive = summaryData?.active_allocated_hours ?? activeHours.toFixed(1);
  const displayTotal = summaryData?.total_allocated_hours ?? totalHours.toFixed(1);

  return (
    <div className="stats-grid" id="summary-stats-grid">
      <div className="stat-card" id="stat-total-assignments">
        <div className="stat-header">
          <span className="stat-label">Total Assignments</span>
        </div>
        <div className="stat-value">{totalCount}</div>
        <div className="stat-subtext">Current view count</div>
      </div>

      <div className="stat-card" id="stat-active-hours">
        <div className="stat-header">
          <span className="stat-label">Active Workload</span>
        </div>
        <div className="stat-value">{displayActive}h</div>
        <div className="stat-subtext">Status = ACTIVE</div>
      </div>

      <div className="stat-card" id="stat-total-hours">
        <div className="stat-header">
          <span className="stat-label">Total Allocated</span>
        </div>
        <div className="stat-value">{displayTotal}h</div>
        <div className="stat-subtext">All statuses combined</div>
      </div>
    </div>
  );
}
