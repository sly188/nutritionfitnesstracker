import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { workoutAPI, weightAPI, nutritionAPI, goalsAPI } from '../../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [workouts, setWorkouts] = useState([]);
  const [weights, setWeights] = useState([]);
  const [nutrition, setNutrition] = useState([]);
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [w, wt, n, g] = await Promise.all([
        workoutAPI.getAll(30),
        weightAPI.getAll(90),
        nutritionAPI.getAll(30),
        goalsAPI.getAll(),
      ]);
      setWorkouts(w.data);
      setWeights(wt.data);
      setNutrition(n.data);
      setGoals(g.data);
    } catch (err) {
      console.error('Error loading data:', err);
    }
    setLoading(false);
  };

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;

  const chartData = weights.map((w) => ({
    date: new Date(w.date).toLocaleDateString(),
    weight: w.weight,
  }));

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Fitness Dashboard</h1>
        <button
          onClick={() => {
            logout();
            navigate('/login');
          }}
          style={{ padding: '8px 16px' }}
        >
          Logout
        </button>
      </div>

      <nav style={{ marginBottom: '20px', borderBottom: '1px solid #ccc', paddingBottom: '10px' }}>
        <button onClick={() => navigate('/')} style={{ marginRight: '10px' }}>
          Dashboard
        </button>
        <button onClick={() => navigate('/workouts')} style={{ marginRight: '10px' }}>
          Workouts
        </button>
        <button onClick={() => navigate('/templates')} style={{ marginRight: '10px' }}>
          Templates
        </button>
        <button onClick={() => navigate('/nutrition')} style={{ marginRight: '10px' }}>
          Nutrition
        </button>
        <button onClick={() => navigate('/weight')} style={{ marginRight: '10px' }}>
          Weight
        </button>
        <button onClick={() => navigate('/goals')} style={{ marginRight: '10px' }}>
          Goals
        </button>
      </nav>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '20px' }}>
        <div style={{ border: '1px solid #ccc', padding: '15px' }}>
          <h3>{workouts.length}</h3>
          <p>Workouts (30 days)</p>
        </div>
        <div style={{ border: '1px solid #ccc', padding: '15px' }}>
          <h3>{nutrition.length}</h3>
          <p>Nutrition Logs</p>
        </div>
        <div style={{ border: '1px solid #ccc', padding: '15px' }}>
          <h3>{weights.length}</h3>
          <p>Weight Entries</p>
        </div>
        <div style={{ border: '1px solid #ccc', padding: '15px' }}>
          <h3>{goals.filter((g) => !g.completed).length}</h3>
          <p>Active Goals</p>
        </div>
      </div>

      {weights.length > 0 && (
        <div style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px' }}>
          <h2>Weight Progress</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="weight" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div style={{ border: '1px solid #ccc', padding: '15px' }}>
        <h2>Recent Workouts</h2>
        {workouts.length === 0 ? (
          <p>No workouts yet</p>
        ) : (
          <ul>
            {workouts.slice(0, 5).map((w) => (
              <li key={w.id} style={{ marginBottom: '10px' }}>
                {new Date(w.date).toLocaleDateString()} - {w.exercises.length} exercises
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}