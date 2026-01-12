import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const authAPI = {
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  logout: () => api.post('/auth/logout'),
};

// Workout endpoints
export const workoutAPI = {
  create: (data) => api.post('/workouts', data),
  getAll: (days = 30) => api.get(`/workouts?days=${days}`),
  getOne: (id) => api.get(`/workouts/${id}`),
  update: (id, data) => api.put(`/workouts/${id}`, data),
  delete: (id) => api.delete(`/workouts/${id}`),
};

// Template endpoints
export const templateAPI = {
  create: (data) => api.post('/templates', data),
  getAll: () => api.get('/templates'),
  getOne: (id) => api.get(`/templates/${id}`),
  update: (id, data) => api.put(`/templates/${id}`, data),
  delete: (id) => api.delete(`/templates/${id}`),
};

// Nutrition endpoints
export const nutritionAPI = {
  create: (data) => api.post('/nutrition', data),
  getAll: (days = 30) => api.get(`/nutrition?days=${days}`),
  getOne: (id) => api.get(`/nutrition/${id}`),
  update: (id, data) => api.put(`/nutrition/${id}`, data),
  delete: (id) => api.delete(`/nutrition/${id}`),
};

// Weight endpoints
export const weightAPI = {
  create: (data) => api.post('/weight', data),
  getAll: (days = 90) => api.get(`/weight?days=${days}`),
  getOne: (id) => api.get(`/weight/${id}`),
  update: (id, data) => api.put(`/weight/${id}`, data),
  delete: (id) => api.delete(`/weight/${id}`),
};

// Goals endpoints
export const goalsAPI = {
  create: (data) => api.post('/goals', data),
  getAll: () => api.get('/goals'),
  getOne: (id) => api.get(`/goals/${id}`),
  update: (id, data) => api.put(`/goals/${id}`, data),
  delete: (id) => api.delete(`/goals/${id}`),
};

export default api;