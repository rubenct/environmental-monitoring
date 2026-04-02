import type { MeasurementFilters, Measurement, Stats, TimeseriesBucket } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

function formatDateLocal(date: Date): string {
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

function buildQuery(filters: MeasurementFilters): URLSearchParams {
  const params = new URLSearchParams();
  if (filters.start) params.set('start', formatDateLocal(filters.start));
  if (filters.end) params.set('end', formatDateLocal(filters.end));
  if (filters.device_id) params.set('device_id', filters.device_id);
  if (filters.interval) params.set('interval', filters.interval);
  return params;
}

async function apiFetch<T>(endpoint: string, params?: URLSearchParams): Promise<T> {
  const url = `${API_BASE}${endpoint}${params ? `?${params}` : ''}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  return response.json();
}

export async function fetchStats(filters: MeasurementFilters): Promise<Stats> {
  return apiFetch<Stats>('/measurements/stats', buildQuery(filters));
}

export async function fetchTimeseries(filters: MeasurementFilters): Promise<TimeseriesBucket[]> {
  return apiFetch<TimeseriesBucket[]>('/measurements/timeseries', buildQuery(filters));
}

export async function fetchMeasurements(filters: MeasurementFilters): Promise<Measurement[]> {
  return apiFetch<Measurement[]>('/measurements', buildQuery(filters));
}
