import React from 'react';

export default function ErrorState({ error, onRetry, currentUser }) {
  const isAuthError = error?.status === 401 || error?.status === 403;

  return (
    <div className="error-state" id="error-state-view">
      <h3>
        {isAuthError
          ? `Access Denied (${error?.status || '403'})`
          : 'Failed to Load Data'}
      </h3>
      <p>
        {error?.message || 'Error communicating with backend API.'}
      </p>

      {currentUser?.id === 'unauthenticated' && (
        <p style={{ color: 'var(--text-muted)', fontSize: '12px', marginBottom: '14px' }}>
          Current user is set to Guest (No Token). Select an authenticated user from the top menu to view assignments.
        </p>
      )}

      <button id="btn-retry-fetch" className="btn-retry" onClick={onRetry}>
        Retry Request
      </button>
    </div>
  );
}
