import React, { useState } from 'react';

export default function CreateAssignmentModal({ isOpen, onClose, employees, onCreated }) {
  const [title, setTitle] = useState('');
  const [employeeId, setEmployeeId] = useState('');
  const [hours, setHours] = useState('10.0');
  const [status, setStatus] = useState('ACTIVE');
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  // Synchronize employeeId when employees list arrives or modal opens
  React.useEffect(() => {
    if (employees && employees.length > 0) {
      if (!employeeId || !employees.some((e) => String(e.id) === String(employeeId))) {
        setEmployeeId(employees[0].id);
      }
    }
  }, [employees, employeeId, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg(null);

    const parsedHours = parseFloat(hours);
    if (!title.trim()) {
      setErrorMsg('Title is required.');
      return;
    }

    const selectedEmpId = employeeId
      ? parseInt(employeeId, 10)
      : (employees[0]?.id ? parseInt(employees[0].id, 10) : null);

    if (!selectedEmpId || isNaN(selectedEmpId)) {
      setErrorMsg('Please select an employee.');
      return;
    }

    if (isNaN(parsedHours) || parsedHours < 0.5) {
      setErrorMsg('Hours must be at least 0.5.');
      return;
    }
    if (parsedHours > 168) {
      setErrorMsg('Hours cannot exceed 168.');
      return;
    }

    setSubmitting(true);
    try {
      await onCreated({
        title: title.trim(),
        employee: selectedEmpId,
        hours: parsedHours,
        status,
      });
      setTitle('');
      setHours('10.0');
      onClose();
    } catch (err) {
      setErrorMsg(err.message || 'Failed to create assignment');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" id="create-modal-overlay">
      <div className="modal-box" id="create-assignment-modal">
        <div className="modal-header">
          <h3>Create New Assignment</h3>
          <button className="btn-close" onClick={onClose} disabled={submitting}>
            Cancel
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-field">
            <label htmlFor="create-title">Title:</label>
            <input
              id="create-title"
              type="text"
              placeholder="e.g. Cache Layer Optimization"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={submitting}
              autoFocus
            />
          </div>

          <div className="form-field">
            <label htmlFor="create-employee">Assigned Employee:</label>
            <select
              id="create-employee"
              value={employeeId || (employees[0]?.id || '')}
              onChange={(e) => setEmployeeId(e.target.value)}
              disabled={submitting}
            >
              {employees.map((emp) => (
                <option key={emp.id} value={emp.id}>
                  {emp.name} ({emp.department_code})
                </option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-field">
              <label htmlFor="create-hours">Allocated Hours:</label>
              <input
                id="create-hours"
                type="number"
                step="0.5"
                value={hours}
                onChange={(e) => setHours(e.target.value)}
                disabled={submitting}
              />
            </div>

            <div className="form-field">
              <label htmlFor="create-status">Status:</label>
              <select
                id="create-status"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                disabled={submitting}
              >
                <option value="ACTIVE">ACTIVE</option>
                <option value="ON_HOLD">ON_HOLD</option>
                <option value="COMPLETED">COMPLETED</option>
              </select>
            </div>
          </div>

          {errorMsg && (
            <div className="modal-error-box" id="create-error-msg">
              Error: {errorMsg}
            </div>
          )}

          <div className="modal-actions">
            <button
              type="submit"
              id="btn-submit-assignment"
              className="btn-primary"
              disabled={submitting}
            >
              {submitting ? 'Creating...' : 'Create Assignment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
