import { describe, it, expect } from 'vitest';
import type { Stats, TimeseriesBucket, MeasurementFilters } from './index';

describe('Types', () => {
  it('defines Measurement interface', () => {
    const measurement = {
      id: '123',
      timestamp: '2024-01-01T00:00:00Z',
      temperature: 25.5,
      humidity: 60,
      device_id: 'sensor-01',
    };
    expect(measurement.id).toBe('123');
  });

  it('defines Stats interface', () => {
    const stats: Stats = {
      start: '2024-01-01T00:00:00Z',
      end: '2024-01-02T00:00:00Z',
      device_id: 'sensor-01',
      temperature: { avg: 25, min: 20, max: 30 },
      humidity: { avg: 60, min: 50, max: 70 },
    };
    expect(stats.temperature.avg).toBe(25);
  });

  it('defines TimeseriesBucket interface', () => {
    const bucket: TimeseriesBucket = {
      timestamp: '2024-01-01T00:00:00Z',
      avg_temperature: 25,
      avg_humidity: 60,
      count: 10,
    };
    expect(bucket.count).toBe(10);
  });

  it('defines MeasurementFilters interface', () => {
    const filters: MeasurementFilters = {
      start: new Date('2024-01-01'),
      end: new Date('2024-01-02'),
      device_id: 'sensor-01',
      interval: 'hour',
    };
    expect(filters.interval).toBe('hour');
  });
});
