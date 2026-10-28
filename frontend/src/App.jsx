import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import SummaryStats from './components/SummaryStats';
import DepartmentFilter from './components/DepartmentFilter';
import AssignmentCard from './components/AssignmentCard';
import CreateAssignmentModal from './components/CreateAssignmentModal';
import LoadingState from './components/LoadingState';
import EmptyState from './components/EmptyState';
import ErrorState from './components/ErrorState';
import NetworkInspector from './components/NetworkInspector';
import {
  getAssignments,
  getEmployees,
  getDepartmentSummary,
  createAssignment,
  updateAssignment,
  DEMO_USERS,
} from './services/api';
import './App.css';

export default function App() {
  // State: Active User for Token Auth
  const [currentUser, setCurrentUser] = useState(DEMO_USERS[0]); // Alice Chen (ENG)

  // State: Filtering & Data
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [selectedStatus, setSelectedStatus] = useState('ALL');
  const [assignments, setAssignments] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [summaryData, setSummaryData] = useState(null);

  // State: UI Modals & Loading
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [networkTraces, setNetworkTraces] = useState([]);
  const [isOnline, setIsOnline] = useState(true);

  // Appends network call to trace drawer for Block 4/5 inspection
  const addTrace = useCallback((trace) => {
    setNetworkTraces((prev) => [trace, ...prev.slice(0, 19)]);
  }, []);

  // Primary data loader
  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const [fetchedAssignments, summary, fetchedEmployees] = await Promise.all([
        getAssignments(selectedDept, selectedStatus, currentUser.token, addTrace),
        getDepartmentSummary(selectedDept, currentUser.token),
        getEmployees(currentUser.token),
      ]);

      setAssignments(fetchedAssignments);
      setSummaryData(summary);
      if (fetchedEmployees && fetchedEmployees.length > 0) {
        setEmployees(fetchedEmployees);
      }
      setIsOnline(true);
    } catch (err) {
      console.error('API Fetch failed:', err);
      setError(err);
      if (err.status === 0) {
        setIsOnline(false);
      }
    } finally {
      setLoading(false);
    }
  }, [selectedDept, selectedStatus, currentUser, addTrace]);

  // Trigger API fetch on mount and whenever department, status, or user changes
  useEffect(() => {
    loadData();
  }, [loadData]);

  // Handle switching active demo user
  const handleUserChange = (userId) => {
    const selected = DEMO_USERS.find((u) => u.id === userId) || DEMO_USERS[0];
    setCurrentUser(selected);
  };

  // Handle updating assignment (hours and/or status)
  const handleUpdateAssignment = async (id, updateData) => {
    const updated = await updateAssignment(id, updateData, currentUser.token, addTrace);
    setAssignments((prev) =>
      prev.map((item) => (item.id === id ? { ...item, ...updated } : item))
    );
    const summary = await getDepartmentSummary(selectedDept, currentUser.token);
    setSummaryData(summary);
  };

  // Handle creating new assignment (POST)
  const handleCreateAssignment = async (newAssignmentData) => {
    const created = await createAssignment(newAssignmentData, currentUser.token, addTrace);
    setAssignments((prev) => [created, ...prev.filter((a) => a.id !== created.id)]);
    await loadData();
  };

  return (
    <div className="app-container" id="workload-tracker-app">
      {/* Header with User Switcher */}
      <Header
        currentUser={currentUser}
        onUserChange={handleUserChange}
        isOnline={isOnline}
      />

      {/* Summary KPI Cards */}
      <SummaryStats assignments={assignments} summaryData={summaryData} />

      {/* Department & Status Filter Toolbar with Add Button */}
      <DepartmentFilter
        selectedDept={selectedDept}
        onSelectDept={setSelectedDept}
        selectedStatus={selectedStatus}
        onSelectStatus={setSelectedStatus}
        onOpenCreate={() => setIsCreateOpen(true)}
        onRefresh={loadData}
        loading={loading}
      />

      {/* Conditional Rendering (Loading, Error, Empty, List) */}
      <main id="main-content">
        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState
            error={error}
            onRetry={loadData}
            currentUser={currentUser}
          />
        ) : assignments.length === 0 ? (
          <EmptyState
            department={selectedDept}
            onResetFilter={() => {
              setSelectedDept('ALL');
              setSelectedStatus('ALL');
            }}
          />
        ) : (
          <div className="assignment-grid" id="assignment-list-view">
            {assignments.map((assignment) => (
              <AssignmentCard
                key={assignment.id}
                assignment={assignment}
                onUpdate={handleUpdateAssignment}
              />
            ))}
          </div>
        )}
      </main>

      {/* Assignment Creation Modal */}
      <CreateAssignmentModal
        isOpen={isCreateOpen}
        onClose={() => setIsCreateOpen(false)}
        employees={employees}
        onCreated={handleCreateAssignment}
      />

      {/* Live Network & Request Inspector */}
      <NetworkInspector traces={networkTraces} />
    </div>
  );
}
