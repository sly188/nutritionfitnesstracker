// src/components/Nutrition/NutritionLog.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { nutritionAPI } from '../../services/api';

export default function NutritionLog() {
  const [logs, setLogs] = useState([]);
  const [protein, setProtein] = useState('');
  const [carbs, setCarbs] = useState('');
  const [fats, setFats] = useState('');
  const [calories, setCalories] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const res = await nutritionAPI.getAll(30);
      setLogs(res.data);
    } catch (err) {
      console.error('Error loading nutrition logs:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await nutritionAPI.create({
        protein: parseFloat(protein),
        carbs: parseFloat(carbs),
        fats: parseFloat(fats),
        calories: parseFloat(calories),
      });
      setProtein('');
      setCarbs('');
      setFats('');
      setCalories('');
      loadLogs();
      alert('Nutrition logged!');
    } catch (err) {
      alert('Error logging nutrition');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this log?')) {
      try {
        await nutritionAPI.delete(id);
        loadLogs();
      } catch (err) {
        alert('Error deleting log');
      }
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Nutrition Tracker</h1>
      <button onClick={() => navigate('/')} style={{ marginBottom: '20px' }}>
        ← Back to Dashboard
      </button>

      <div style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px', maxWidth: '400px' }}>
        <h2>Log Macros</h2>
        <form onSubmit={handleSubmit}>
          <input type="number" placeholder="Protein (g)" value={protein} onChange={(e) => setProtein(e.target.value)} required style={{ width: '100%', padding: '5px', marginBottom: '10px' }} />
          <input type="number" placeholder="Carbs (g)" value={carbs} onChange={(e) => setCarbs(e.target.value)} required style={{ width: '100%', padding: '5px', marginBottom: '10px' }} />
          <input type="number" placeholder="Fats (g)" value={fats} onChange={(e) => setFats(e.target.value)} required style={{ width: '100%', padding: '5px', marginBottom: '10px' }} />
          <input type="number" placeholder="Calories" value={calories} onChange={(e) => setCalories(e.target.value)} required style={{ width: '100%', padding: '5px', marginBottom: '10px' }} />
          <button type="submit" style={{ width: '100%', padding: '8px', backgroundColor: '#4CAF50', color: 'white' }}>
            Log
          </button>
        </form>
      </div>

      <div>
        {logs.length === 0 ? (
          <p>No nutrition logs yet</p>
        ) : (
          logs.map((log) => (
            <div key={log.id} style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <h3>{new Date(log.date).toLocaleDateString()}</h3>
                  <p>P: {log.protein}g | C: {log.carbs}g | F: {log.fats}g | {log.calories} cal</p>
                </div>
                <button onClick={() => handleDelete(log.id)} style={{ padding: '8px', height: '30px' }}>
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
