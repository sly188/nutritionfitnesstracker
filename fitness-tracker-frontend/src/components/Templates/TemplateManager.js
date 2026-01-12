import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { templateAPI } from '../../services/api';

const DEFAULT_NAME = 'Default Template';

export default function TemplateManager() {
  const [templates, setTemplates] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: DEFAULT_NAME,
    exercises: [{ name: '', sets: 3, reps: '8-10' }],
  });
  const nameInputRef = useRef(null);
  const navigate = useNavigate();

  const buttonStyle = {
    padding: '10px 20px',
    minWidth: '180px',
    marginBottom: '20px',
    border: '1px solid #ccc',
    borderRadius: '6px',
    background: 'white',
    cursor: 'pointer',
  };

  useEffect(() => {
    loadTemplates();
  }, []);

  useEffect(() => {
    if (showForm && nameInputRef.current) {
      nameInputRef.current.focus();
      nameInputRef.current.select();
    }
  }, [showForm]);

  const loadTemplates = async () => {
    try {
      const res = await templateAPI.getAll();
      setTemplates(res.data);
    } catch (err) {
      console.error('Error loading templates:', err);
    }
  };

  const handleAddExercise = () => {
    setFormData({
      ...formData,
      exercises: [...formData.exercises, { name: '', sets: 3, reps: '8-10' }],
    });
  };

  const handleExerciseChange = (idx, field, value) => {
    const newExercises = [...formData.exercises];
    newExercises[idx][field] = field === 'sets' ? parseInt(value, 10) : value;
    setFormData({ ...formData, exercises: newExercises });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        name: (formData.name || '').trim() || DEFAULT_NAME,
      };
      await templateAPI.create(payload);
      setFormData({ name: DEFAULT_NAME, exercises: [{ name: '', sets: 3, reps: '8-10' }] });
      setShowForm(false);
      loadTemplates();
      alert('Template created!');
    } catch (err) {
      alert('Error creating template');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this template?')) {
      try {
        await templateAPI.delete(id);
        loadTemplates();
      } catch (err) {
        alert('Error deleting template');
      }
    }
  };

  const openForm = () => {
    setFormData({ name: DEFAULT_NAME, exercises: [{ name: '', sets: 3, reps: '8-10' }] });
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
    setFormData({ name: DEFAULT_NAME, exercises: [{ name: '', sets: 3, reps: '8-10' }] });
  };

  return (
    <div style={{ padding: '10px' }}>
      <h1>Workout Templates</h1>

      {/* Back button */}
      <button
        onClick={() => navigate('/')}
        style={buttonStyle}
      >
        ← Back to Dashboard
      </button>

      {/* New Template button */}
      <button
        onClick={() => (showForm ? closeForm() : openForm())}
        style={{ ...buttonStyle, marginLeft: '10px' }}
      >
        {showForm ? 'Cancel' : '+ New Template'}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit} style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px' }}>
          <div style={{ marginBottom: '10px' }}>
            <label>Template Name: </label>
            <input
              ref={nameInputRef}
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              style={{ width: '100%', padding: '5px' }}
            />
          </div>

          {formData.exercises.map((ex, idx) => (
            <div key={idx} style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f5f5f5' }}>
              <input
                type="text"
                placeholder="Exercise name"
                value={ex.name}
                onChange={(e) => handleExerciseChange(idx, 'name', e.target.value)}
                required
                style={{ width: '100%', padding: '5px', marginBottom: '5px' }}
              />
              <input
                type="number"
                placeholder="Sets"
                value={ex.sets}
                onChange={(e) => handleExerciseChange(idx, 'sets', e.target.value)}
                style={{ width: '48%', padding: '5px', marginRight: '4%' }}
              />
              <input
                type="text"
                placeholder="Reps (e.g., 8-10)"
                value={ex.reps}
                onChange={(e) => handleExerciseChange(idx, 'reps', e.target.value)}
                style={{ width: '48%', padding: '5px' }}
              />
            </div>
          ))}

          <button type="button" onClick={handleAddExercise} style={{ marginBottom: '10px', padding: '5px 10px' }}>
            + Add Exercise
          </button>

          <div>
            <button
              type="submit"
              style={{ padding: '8px 16px', marginRight: '10px', backgroundColor: '#4CAF50', color: 'white' }}
            >
              Create Template
            </button>
          </div>
        </form>
      )}

      <div>
        {templates.length === 0 ? (
          <p>No templates yet</p>
        ) : (
          templates.map((t) => (
            <div key={t.id} style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <h3>{t.name}</h3>
                  {t.exercises.map((ex, i) => (
                    <div key={i} style={{ marginLeft: '20px', fontSize: '14px' }}>
                      {ex.name} - {ex.sets} x {ex.reps}
                    </div>
                  ))}
                </div>
                <button onClick={() => handleDelete(t.id)} style={{ padding: '8px', height: '30px' }}>
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
