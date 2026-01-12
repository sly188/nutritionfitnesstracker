import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { workoutAPI } from '../../services/api';

export default function WorkoutList() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadWorkouts();
  }, []);

  const loadWorkouts = async () => {
    try {
      const res = await workoutAPI.getAll(30);
      setWorkouts(res.data);
    } catch (err) {
      console.error('Error loading workouts:', err);
    }
    setLoading(false);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this workout?')) {
      try {
        await workoutAPI.delete(id);
        setWorkouts(workouts.filter((w) => w.id !== id));
      } catch (err) {
        alert('Error deleting workout');
      }
    }
  };

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Workouts</h1>
        <button onClick={() => navigate('/workouts/log')} style={{ padding: '8px 16px' }}>
          Log Workout
        </button>
      </div>

      <button onClick={() => navigate('/')} style={{ marginBottom: '20px' }}>
        ← Back to Dashboard
      </button>

      {workouts.length === 0 ? (
        <p>No workouts logged yet</p>
      ) : (
        <div>
          {workouts.map((w) => (
            <div key={w.id} style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <h3>{new Date(w.date).toLocaleDateString()}</h3>
                  <p>{w.exercises.length} exercises</p>
                  {w.exercises.map((ex, i) => (
                    <div key={i} style={{ marginLeft: '20px', fontSize: '14px' }}>
                      <strong>{ex.name}</strong> - {ex.sets.length} sets
                    </div>
                  ))}
                </div>
                <button onClick={() => handleDelete(w.id)} style={{ padding: '8px', height: '30px' }}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

