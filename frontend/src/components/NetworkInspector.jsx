import React, { useState } from 'react';

export default function NetworkInspector({ traces }) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="network-inspector" id="network-inspector-drawer">
      <div
        className="inspector-header"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="inspector-title">
          <span>Network & Request Inspector</span>
          <span className="inspector-badge">{traces.length} requests</span>
        </div>
        <button style={{ padding: '2px 8px', fontSize: '11px' }}>
          {isOpen ? 'Collapse' : 'Expand'}
        </button>
      </div>

      {isOpen && (
        <div style={{ overflowX: 'auto', maxHeight: '220px', overflowY: 'auto' }}>
          <table className="trace-table" id="trace-history-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Method</th>
                <th>Endpoint</th>
                <th>Latency</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {traces.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '12px', color: 'var(--text-muted)' }}>
                    No network requests recorded.
                  </td>
                </tr>
              ) : (
                traces.map((trace, idx) => (
                  <tr key={idx}>
                    <td>{trace.timestamp}</td>
                    <td className="method-tag">{trace.method}</td>
                    <td>{trace.url}</td>
                    <td>{trace.latency}</td>
                    <td className="status-badge">
                      {trace.status ? `${trace.status} ${trace.statusText}` : 'Failed'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
