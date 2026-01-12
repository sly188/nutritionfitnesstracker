import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { workoutAPI, templateAPI } from '../../services/api';

export default function LogWorkout() {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [exercises, setExercises] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const res = await templateAPI.getAll();
      setTemplates(res.data);
    } catch (err) {
      console.error('Error loading templates:', err);
    }
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    const exs = template.exercises.map((e) => ({
      name: e.name,
      sets: Array(e.sets)
        .fill(null)
        .map((_, i) => ({ set_number: i + 1, reps: parseInt(e.reps) || 0, weight: 0 })),
    }));
    setExercises(exs);
  };

  const handleSetChange = (exIndex, setIndex, field, value) => {
    const newExercises = [...exercises];
    newExercises[exIndex].sets[setIndex][field] = field === 'reps' ? parseInt(value) : parseFloat(value);
    setExercises(newExercises);
  };

  const handleAddSet = (exIndex) => {
    const newExercises = [...exercises];
    const lastSet = newExercises[exIndex].sets[newExercises[exIndex].sets.length - 1];
    newExercises[exIndex].sets.push({
      set_number: lastSet.set_number + 1,
      reps: lastSet.reps,
      weight: lastSet.weight,
    });
    setExercises(newExercises);
  };

  const handleSubmit = async () => {
    if (!selectedTemplate || exercises.length === 0) {
      alert('Select a template');
      return;
    }
    try {
      await workoutAPI.create({
        template_id: selectedTemplate.id,
        exercises: exercises.map((e) => ({ name: e.name, sets: e.sets })),
      });
      alert('Workout logged!');
      navigate('/workouts');
    } catch (err) {
      alert('Error logging workout');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Log Workout</h1>
      <button onClick={() => navigate('/workouts')} style={{ marginBottom: '20px' }}>
        ← Back to Workouts
      </button>

      <div style={{ marginBottom: '20px' }}>
        <label>Select Template: </label>
        <select onChange={(e) => handleTemplateSelect(templates.find((t) => t.id === parseInt(e.target.value)))} style={{ padding: '5px' }}>
          <option value="">Choose template...</option>
          {templates.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name}
            </option>
          ))}
        </select>
      </div>

      {selectedTemplate && exercises.length > 0 && (
        <div>
          {exercises.map((ex, exIdx) => (
            <div key={exIdx} style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '15px' }}>
              <h3>{ex.name}</h3>
              {ex.sets.map((s, sIdx) => (
                <div key={sIdx} style={{ display: 'flex', gap: '10px', marginBottom: '5px', alignItems: 'center' }}>
                  <span>Set {s.set_number}:</span>
                  <input
                    type="number"
                    placeholder="Reps"
                    value={s.reps}
                    onChange={(e) => handleSetChange(exIdx, sIdx, 'reps', e.target.value)}
                    style={{ width: '80px', padding: '5px' }}
                  />
                  <input
                    type="number"
                    placeholder="Weight (lbs)"
                    value={s.weight}
                    onChange={(e) => handleSetChange(exIdx, sIdx, 'weight', e.target.value)}
                    style={{ width: '100px', padding: '5px' }}
                  />
                </div>
              ))}
              <button onClick={() => handleAddSet(exIdx)} style={{ marginTop: '10px', padding: '5px 10px' }}>
                + Add Set
              </button>
            </div>
          ))}

          <button onClick={handleSubmit} style={{ padding: '10px 20px', backgroundColor: '#4CAF50', color: 'white' }}>
            Save Workout
          </button>
        </div>
      )}
    </div>
  );
}