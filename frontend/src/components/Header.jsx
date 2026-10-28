import React from 'react';

export default function Header({ currentUser, onUserChange, isOnline }) {
  return (
    <header className="header" id="app-header">
      <div className="brand-section">
        <div className="brand-title">
          <h1>Workload Tracker</h1>
          <p>Full-Stack Dashboard (React + Django REST Framework)</p>
        </div>
      </div>

      <div className="header-controls">
        <div className="status-pill" id="backend-status-pill">
          {isOnline ? '[API Connected]' : '[API Offline]'}
        </div>

        <div className="user-switcher" id="user-switcher">
          <label htmlFor="user-select">User:</label>
          <select
            id="user-select"
            value={currentUser.id}
            onChange={(e) => onUserChange(e.target.value)}
          >
            <option value="alice_eng">Alice Chen (ENG)</option>
            <option value="charlie_pm">Charlie Kim (PM)</option>
            <option value="admin_lead">Admin Lead (Staff)</option>
            <option value="unauthenticated">Guest (No Auth Token)</option>
          </select>
        </div>
      </div>
    </header>
  );
}
