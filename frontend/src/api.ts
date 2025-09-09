import axios from 'axios'
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000', timeout: 120000 })
export async function predict(payload: { headline?: string; body?: string }) {
  const { data } = await api.post('/predict', payload)
  return data as { label: string; proba: number; top_features: string[] }
}
export async function health() { const { data } = await api.get('/health'); return data }
export async function feedback(payload: { headline?: string; body?: string; predicted: string; correct_label: string }) {
  const { data } = await api.post('/feedback', payload); return data
}
