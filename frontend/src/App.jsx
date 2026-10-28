import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import SummaryStats from './components/SummaryStats';
import DepartmentFilter from './components/DepartmentFilter';
import AssignmentCard from './components/AssignmentCard';
import LoadingState from './components/LoadingState';
import EmptyState from './components/EmptyState';
import ErrorState from './components/ErrorState';
import NetworkInspector from './components/NetworkInspector';
import {
  getAssignments,
  getDepartmentSummary,
  updateAssignmentHours,
  DEMO_USERS,
} from './services/api';
import './App.css';

export default function App() {
  // State: Active User for Token Auth
  const [currentUser, setCurrentUser] = useState(DEMO_USERS[0]); // Alice Chen (ENG)

  // State: Filter & Data
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [assignments, setAssignments] = useState([]);
  const [summaryData, setSummaryData] = useState(null);

  // State: Network / Async UI States
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [networkTraces, setNetworkTraces] = useState([]);
  const [isOnline, setIsOnline] = useState(true);

  // Appends network call to trace drawer for Block 4/5 inspection
  const addTrace = useCallback((trace) => {
    setNetworkTraces((prev) => [trace, ...prev.slice(0, 19)]);
  }, []);

  // Primary data loader (Block 2 & 4: useEffect & async/await API call)
  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const [fetchedAssignments, summary] = await Promise.all([
        getAssignments(selectedDept, currentUser.token, addTrace),
        getDepartmentSummary(selectedDept, currentUser.token),
      ]);

      setAssignments(fetchedAssignments);
      setSummaryData(summary);
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
  }, [selectedDept, currentUser, addTrace]);

  // Trigger API fetch on mount and whenever department or active user changes
  useEffect(() => {
    loadData();
  }, [loadData]);

  // Handle switching active demo user
  const handleUserChange = (userId) => {
    const selected = DEMO_USERS.find((u) => u.id === userId) || DEMO_USERS[0];
    setCurrentUser(selected);
  };

  // Handle updating assignment hours (PATCH request)
  const handleUpdateHours = async (id, newHours) => {
    const updated = await updateAssignmentHours(id, newHours, currentUser.token, addTrace);
    // Optimistically/smoothly update local assignment state
    setAssignments((prev) =>
      prev.map((item) => (item.id === id ? { ...item, hours: updated.hours } : item))
    );
    // Refresh summary metrics
    const summary = await getDepartmentSummary(selectedDept, currentUser.token);
    setSummaryData(summary);
  };

  return (
    <div className="app-container" id="workload-tracker-app">
      {/* Block 1: Header Component with User Switcher */}
      <Header
        currentUser={currentUser}
        onUserChange={handleUserChange}
        isOnline={isOnline}
      />

      {/* Block 2: Workload Summary KPI Cards */}
      <SummaryStats assignments={assignments} summaryData={summaryData} />

      {/* Block 3: Department Filter Toolbar */}
      <DepartmentFilter
        selectedDept={selectedDept}
        onSelectDept={setSelectedDept}
        onRefresh={loadData}
        loading={loading}
      />

      {/* Block 2 & 4: Conditional Rendering (Loading, Error, Empty, List) */}
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
            onResetFilter={() => setSelectedDept('ALL')}
          />
        ) : (
          <div className="assignment-grid" id="assignment-list-view">
            {assignments.map((assignment) => (
              <AssignmentCard
                key={assignment.id}
                assignment={assignment}
                onUpdateHours={handleUpdateHours}
              />
            ))}
          </div>
        )}
      </main>

      {/* Block 5: Live Network Request & Response Tracer */}
      <NetworkInspector traces={networkTraces} />
    </div>
  );
}
