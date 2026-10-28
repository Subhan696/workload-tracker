import React, { useState } from 'react';

export default function AssignmentCard({ assignment, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false);
  const [hoursInput, setHoursInput] = useState(assignment.hours);
  const [statusInput, setStatusInput] = useState(assignment.status);
  const [saving, setSaving] = useState(false);
  const [editError, setEditError] = useState(null);

  const handleSave = async () => {
    setEditError(null);
    const parsed = parseFloat(hoursInput);

    if (isNaN(parsed) || parsed < 0) {
      setEditError('Hours cannot be negative.');
      return;
    }
    if (parsed > 168) {
      setEditError('Hours cannot exceed 168.');
      return;
    }

    setSaving(true);
    try {
      await onUpdate(assignment.id, {
        hours: parsed,
        status: statusInput,
      });
      setIsEditing(false);
    } catch (err) {
      setEditError(err.message || 'Failed to update assignment');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setHoursInput(assignment.hours);
    setStatusInput(assignment.status);
    setEditError(null);
    setIsEditing(false);
  };

  return (
    <div className="assignment-card" id={`assignment-card-${assignment.id}`}>
      <div>
        <div className="card-top">
          <h3 className="card-title">{assignment.title}</h3>
          <span className="badge">{assignment.status}</span>
        </div>

        <div className="card-employee">
          <div className="emp-details">
            <h4>{assignment.employee_name || `Employee #${assignment.employee}`}</h4>
            <span>Dept: {assignment.department_code} ({assignment.department_name})</span>
          </div>
        </div>
      </div>

      <div className="card-footer">
        <div className="hours-display">
          <span className="hours-num">{assignment.hours}h</span>
          <span className="hours-label">Allocated Hours</span>
        </div>

        {!isEditing ? (
          <button
            id={`btn-edit-${assignment.id}`}
            className="btn-edit-hours"
            onClick={() => setIsEditing(true)}
          >
            Edit
          </button>
        ) : null}
      </div>

      {isEditing && (
        <div className="edit-hours-form" id={`edit-form-${assignment.id}`}>
          <div className="edit-input-row" style={{ marginBottom: '8px' }}>
            <label style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Hours:</label>
            <input
              id={`input-hours-${assignment.id}`}
              type="number"
              step="0.5"
              value={hoursInput}
              onChange={(e) => setHoursInput(e.target.value)}
              disabled={saving}
              style={{ width: '70px' }}
              autoFocus
            />

            <label style={{ fontSize: '11px', color: 'var(--text-muted)', marginLeft: '6px' }}>Status:</label>
            <select
              id={`select-status-${assignment.id}`}
              value={statusInput}
              onChange={(e) => setStatusInput(e.target.value)}
              disabled={saving}
              style={{ fontSize: '11px', padding: '3px 6px' }}
            >
              <option value="ACTIVE">ACTIVE</option>
              <option value="ON_HOLD">ON_HOLD</option>
              <option value="COMPLETED">COMPLETED</option>
            </select>
          </div>

          <div style={{ display: 'flex', gap: '6px' }}>
            <button
              id={`btn-save-${assignment.id}`}
              className="btn-save-sm"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save'}
            </button>
            <button
              id={`btn-cancel-${assignment.id}`}
              className="btn-cancel-sm"
              onClick={handleCancel}
              disabled={saving}
            >
              Cancel
            </button>
          </div>

          {editError && (
            <div className="edit-error-msg" id={`error-msg-${assignment.id}`}>
              Error: {editError}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
