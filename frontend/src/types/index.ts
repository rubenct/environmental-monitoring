export interface Measurement {
  id: string;
  timestamp: string;
  temperature: number;
  humidity: number;
  device_id: string | null;
}

export interface AggregatedStats {
  avg: number | null;
  min: number | null;
  max: number | null;
}

export interface Stats {
  start: string | null;
  end: string | null;
  device_id: string | null;
  temperature: AggregatedStats;
  humidity: AggregatedStats;
}

export interface TimeseriesBucket {
  timestamp: string;
  avg_temperature: number;
  avg_humidity: number;
  count: number;
}

export interface MeasurementFilters {
  start?: Date;
  end?: Date;
  device_id?: string;
  interval?: 'hour' | 'day' | 'week';
}
