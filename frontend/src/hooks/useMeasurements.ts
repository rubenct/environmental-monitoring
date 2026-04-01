import { useState, useEffect, useCallback } from 'react';
import { fetchTimeseries } from '../api/measurements';
import type { MeasurementFilters, Stats, TimeseriesBucket } from '../types';

interface UseMeasurementsResult {
  stats: Stats | null;
  timeseries: TimeseriesBucket[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useMeasurements(filters: MeasurementFilters): UseMeasurementsResult {
  const [timeseries, setTimeseries] = useState<TimeseriesBucket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const calculateStats = (data: TimeseriesBucket[]): Stats | null => {
    if (data.length === 0) {
      return null;
    }

    const temps = data.map((d) => d.avg_temperature);
    const humids = data.map((d) => d.avg_humidity);

    const avg = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length;
    const min = (arr: number[]) => Math.min(...arr);
    const max = (arr: number[]) => Math.max(...arr);

    return {
      start: filters.start?.toISOString() || null,
      end: filters.end?.toISOString() || null,
      device_id: filters.device_id || null,
      temperature: {
        avg: avg(temps),
        min: min(temps),
        max: max(temps),
      },
      humidity: {
        avg: avg(humids),
        min: min(humids),
        max: max(humids),
      },
    };
  };

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const timeseriesData = await fetchTimeseries({
        ...filters,
        interval: filters.interval || 'hour',
      });
      setTimeseries(timeseriesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const stats = calculateStats(timeseries);

  return { stats, timeseries, loading, error, refetch: fetchData };
}
