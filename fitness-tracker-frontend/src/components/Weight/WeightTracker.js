import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { weightAPI } from '../../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const RANGE_OPTIONS = [
  { key: '7', label: '7 Days', days: 7 },
  { key: '30', label: '30 Days', days: 30 },
  { key: '90', label: '90 Days', days: 90 },
  { key: '365', label: '1 Year', days: 365 },
  { key: 'all', label: 'All Time', days: null },
];

export default function WeightTracker() {
  const [logs, setLogs] = useState([]);
  const [weight, setWeight] = useState('');
  const [range, setRange] = useState('all'); 
  const navigate = useNavigate();

  useEffect(() => {
    loadLogsForRange(range);
  }, [range]);

  // Fetch logs from API. If days is null, request all time.
  const loadLogsForRange = async (rangeKey) => {
    try {
      const option = RANGE_OPTIONS.find((o) => o.key === rangeKey);
      // If your API supports a days param, pass it. Use null or 'all' for all time.
      const daysParam = option.days;
      const res = await weightAPI.getAll(daysParam); // weightAPI.getAll(null) should return all logs
      // Ensure we have an array
      const allLogs = res.data || [];
      // Sort by date ascending
      allLogs.sort((a, b) => new Date(a.date) - new Date(b.date));
      // Optionally group by date and keep the latest entry per day
      const grouped = groupLatestPerDay(allLogs);
      setLogs(grouped);
    } catch (err) {
      console.error('Error loading weight logs:', err);
    }
  };

  // Helper: keep only the latest log per calendar day
  const groupLatestPerDay = (entries) => {
    const map = new Map();
    entries.forEach((e) => {
      const day = new Date(e.date).toISOString().slice(0, 10); // YYYY-MM-DD
      // keep the latest by timestamp
      if (!map.has(day) || new Date(e.date) > new Date(map.get(day).date)) {
        map.set(day, e);
      }
    });
    // return sorted array by date
    return Array.from(map.values()).sort((a, b) => new Date(a.date) - new Date(b.date));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await weightAPI.create({ weight: parseFloat(weight) });
      setWeight('');
      loadLogsForRange(range);
      alert('Weight logged!');
    } catch (err) {
      alert('Error logging weight');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this log?')) {
      try {
        await weightAPI.delete(id);
        loadLogsForRange(range);
      } catch (err) {
        alert('Error deleting log');
      }
    }
  };

  // Chart data: map to readable date and numeric weight
  const chartData = logs.map((l) => ({
    date: new Date(l.date).toLocaleDateString(),
    weight: l.weight,
  }));

  return (
    <div style={{ padding: '20px' }}>
      <h1>Weight Tracker</h1>
      <button onClick={() => navigate('/')} style={{ marginBottom: '20px' }}>
        ← Back to Dashboard
      </button>

      {/* Range selector */}
      <div style={{ marginBottom: '12px', display: 'flex', gap: '8px', alignItems: 'center' }}>
        {RANGE_OPTIONS.map((opt) => (
          <button
            key={opt.key}
            onClick={() => setRange(opt.key)}
            style={{
              padding: '6px 10px',
              borderRadius: '6px',
              border: range === opt.key ? '2px solid #0713beff' : '1px solid #ccc',
              cursor: 'pointer',
            }}
          >
            {opt.label}
          </button>
        ))}
      </div>

      <div style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px', maxWidth: '400px' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <input
            type="number"
            step="0.1"
            placeholder="Weight (lbs)"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '10px',
              boxSizing: 'border-box',
              height: '44px',
              fontSize: '16px',
              borderRadius: '4px',
              border: '1px solid #ccc',
            }}
          />
          <button
            type="submit"
            style={{
              width: '100%',
              height: '44px',
              padding: '0 16px',
              backgroundColor: '#0713beff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '16px',
              cursor: 'pointer',
            }}
          >
            Log Weight
          </button>
        </form>
      </div>

      {chartData.length > 0 && (
        <div style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px' }}>
          <h2>Progress</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis label={{ value: 'Weight (lbs)', angle: -90, position: 'insideLeft', offset: 10 }} />
              <Tooltip formatter={(value, name) => [value, 'Weight']} />
              <Line type="monotone" dataKey="weight" name="Weight" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div>
        {logs.length === 0 ? (
          <p>No weight logs yet</p>
        ) : (
          logs.map((log) => (
            <div key={log.id} style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #eee', padding: '10px 0' }}>
              <div>
                <span>{new Date(log.date).toLocaleDateString()}</span> - <strong>Weight: {log.weight} lbs</strong>
              </div>
              <button onClick={() => handleDelete(log.id)} style={{ padding: '5px 10px' }}>
                Delete
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
