import axios from 'axios';

const api = axios.create({
<<<<<<< HEAD
  baseURL: import.meta.env.VITE_API_URL || '',
=======
  baseURL: API_BASE,
  timeout: 180000, // 3 minutes — Railway needs time to load HuggingFace models on cold start
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096
  headers: {
    'Content-Type': 'application/json',
  },
});

export const startAssessment = async (userDetails) => {
  const response = await api.post('/api/assessment/start/', userDetails);
  return response.data;
};

export const getQuestions = async (assessmentId) => {
  const response = await api.get(`/api/assessment/${assessmentId}/questions/`);
  return response.data;
};

export const submitResponses = async (assessmentId, responses) => {
  const response = await api.post(`/api/assessment/${assessmentId}/submit/`, { responses });
  return response.data;
};

export const getResults = async (assessmentId) => {
  const response = await api.get(`/api/assessment/${assessmentId}/results/`);
  return response.data;
};

export default api;
