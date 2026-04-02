import type { MeasurementFilters, Measurement, Stats, TimeseriesBucket } from '../types';

// Use environment variable for production, fallback to local
// Vercel: Set VITE_API_BASE_URL=https://alert-forgiveness-production.up.railway.app
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://alert-forgiveness-production.up.railway.app';

function formatDateLocal(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
}

function buildQuery(filters: MeasurementFilters): string {
  const params = new URLSearchParams();
  if (filters.start) params.set('start', formatDateLocal(filters.start));
  if (filters.end) params.set('end', formatDateLocal(filters.end));
  if (filters.device_id) params.set('device_id', filters.device_id);
  if (filters.interval) params.set('interval', filters.interval);
  return params.toString();
}

export async function fetchStats(filters: MeasurementFilters): Promise<Stats> {
  const query = buildQuery(filters);
  const response = await fetch(`${API_BASE}/measurements/stats?${query}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch stats: ${response.statusText}`);
  }
  return response.json();
}

export async function fetchTimeseries(filters: MeasurementFilters): Promise<TimeseriesBucket[]> {
  const query = buildQuery(filters);
  const response = await fetch(`${API_BASE}/measurements/timeseries?${query}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch timeseries: ${response.statusText}`);
  }
  return response.json();
}

export async function fetchMeasurements(filters: MeasurementFilters): Promise<Measurement[]> {
  const query = buildQuery(filters);
  const response = await fetch(`${API_BASE}/measurements?${query}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch measurements: ${response.statusText}`);
  }
  return response.json();
}
