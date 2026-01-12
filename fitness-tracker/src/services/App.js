import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './components/Auth/LoginPage';
import RegisterPage from './components/Auth/RegisterPage';
import Dashboard from './components/Dashboard/Dashboard';
import WorkoutList from './components/Workouts/WorkoutList';
import LogWorkout from './components/Workouts/LogWorkout';
import NutritionLog from './components/Nutrition/NutritionLog';
import WeightTracker from './components/Weight/WeightTracker';
import GoalsPage from './components/Goals/GoalsPage';
import TemplateManager from './components/Templates/TemplateManager';
import './App.css';

function ProtectedRoute({ children }) {
  const { token, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!token) return <Navigate to="/login" />;
  return children;
}

function AppContent() {
  const { token } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        {!token ? (
          <>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </>
        ) : (
          <>
            <Route path="/" element={<Dashboard />} />
            <Route path="/workouts" element={<WorkoutList />} />
            <Route path="/workouts/log" element={<LogWorkout />} />
            <Route path="/nutrition" element={<NutritionLog />} />
            <Route path="/weight" element={<WeightTracker />} />
            <Route path="/goals" element={<GoalsPage />} />
            <Route path="/templates" element={<TemplateManager />} />
            <Route path="*" element={<Navigate to="/" />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;