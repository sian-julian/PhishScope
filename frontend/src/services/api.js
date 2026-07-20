import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeURL = async (url) => {
  try {
    const response = await api.post('/analyze', { url });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Server error occurred.');
    } else if (error.request) {
      throw new Error('Unable to connect to the PhishScope API.');
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};
