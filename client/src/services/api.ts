import axios from 'axios';
import { type ClassifyResponse, type AdviceResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log("TOKEN IN REQUEST!")
  }
  return config;
  console.log("TOKEN NOT IN REQUEST!")
});

// --- Auth API ---
export const authApi = {
  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    const response = await axios.post(`${API_BASE_URL}/token`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

// --- AdaRSS API (requires JWT token) ---
export const adarssApi = {
  classify: async (jobTitle: string, skill: string) => {
    const response = await api.post<ClassifyResponse>('/classify', {
      job_title: jobTitle,
      skill,
    });
    return response.data;
  },

  getAdvice: async (history: string, targetSkill: string) => {
    const response = await api.post<AdviceResponse>('/advice', {
      history,
      target_skill: targetSkill,
    });
    return response.data;
  },
};

export default api;