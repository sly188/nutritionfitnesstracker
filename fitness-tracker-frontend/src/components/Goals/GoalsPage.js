import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { goalsAPI } from '../../services/api';

export default function GoalsPage() {
  const [goals, setGoals] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [goalType, setGoalType] = useState('weight');
  const [targetValue, setTargetValue] = useState('');
  const [period, setPeriod] = useState('month');
  const navigate = useNavigate();

  useEffect(() => {
    loadGoals();
  }, []);

  const loadGoals = async () => {
    try {
      const res = await goalsAPI.getAll();
      setGoals(res.data);
    } catch (err) {
      console.error('Error loading goals:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await goalsAPI.create({ goal_type: goalType, target_value: parseFloat(targetValue), period });
      setGoalType('weight');
      setTargetValue('');
      setPeriod('month');
      setShowForm(false);
      loadGoals();
      alert('Goal created!');
    } catch (err) {
      alert('Error creating goal');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this goal?')) {
      try {
        await goalsAPI.delete(id);
        loadGoals();
      } catch (err) {
        alert('Error deleting goal');
      }
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Goals</h1>
      <button onClick={() => navigate('/')} style={{ marginBottom: '20px' }}>
        ← Back to Dashboard
      </button>

      <button onClick={() => setShowForm(!showForm)} style={{ padding: '8px 16px', marginBottom: '20px' }}>
        {showForm ? 'Cancel' : '+ New Goal'}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit} style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px', maxWidth: '400px' }}>
          <select value={goalType} onChange={(e) => setGoalType(e.target.value)} style={{ width: '100%', padding: '5px', marginBottom: '10px' }}>
            <option value="weight">Weight Loss</option>
            <option value="calories">Daily Calories</option>
            <option value="workout_count">Workouts</option>
          </select>
          <input type="number" placeholder="Target Value" value={targetValue} onChange={(e) => setTargetValue(e.target.value)} required style={{ width: '100%', padding: '5px', marginBottom: '10px' }} />
          <select value={period} onChange={(e) => setPeriod(e.target.value)} style={{ width: '100%', padding: '5px', marginBottom: '10px' }}>
            <option value="month">Monthly</option>
            <option value="year">Yearly</option>
          </select>
          <button type="submit" style={{ width: '100%', padding: '8px', backgroundColor: '#4CAF50', color: 'white' }}>
            Create Goal
          </button>
        </form>
      )}

      <div>
        {goals.length === 0 ? (
          <p>No goals yet</p>
        ) : (
          goals.map((goal) => (
            <div key={goal.id} style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3>{goal.goal_type}</h3>
                  <p>
                    Target: {goal.target_value} ({goal.period}) - Progress: {goal.current_value}
                  </p>
                  <div style={{ width: '300px', height: '20px', backgroundColor: '#eee', borderRadius: '5px', overflow: 'hidden' }}>
                    <div style={{ width: `${Math.min((goal.current_value / goal.target_value) * 100, 100)}%`, height: '100%', backgroundColor: '#4CAF50' }} />
                  </div>
                </div>
                <button onClick={() => handleDelete(goal.id)} style={{ padding: '8px' }}>
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}