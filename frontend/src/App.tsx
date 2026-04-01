import { useState, useMemo } from 'react';
import { subDays } from 'date-fns';
import { Header } from './components/Header/Header';
import { DeviceFilter } from './components/DeviceFilter/DeviceFilter';
import { DateRangePicker } from './components/DateRangePicker/DateRangePicker';
import { StatsPanel } from './components/StatsPanel/StatsPanel';
import { TimeSeriesChart } from './components/TimeSeriesChart/TimeSeriesChart';
import { DataTable } from './components/DataTable/DataTable';
import { useMeasurements } from './hooks/useMeasurements';
import styles from './App.module.css';

const DEVICES = ['sensor-01', 'sensor-02', 'sensor-03'];

export function App() {
  const [deviceId, setDeviceId] = useState('');
  const [startDate, setStartDate] = useState<Date | null>(subDays(new Date(), 7));
  const [endDate, setEndDate] = useState<Date | null>(new Date());
  const [interval, setInterval] = useState<'hour' | 'day' | 'week'>('hour');

  const filters = useMemo(
    () => ({
      device_id: deviceId || undefined,
      start: startDate || undefined,
      end: endDate || undefined,
      interval,
    }),
    [deviceId, startDate, endDate, interval]
  );

  const { stats, timeseries, loading, error, refetch } = useMeasurements(filters);

  return (
    <div className={styles.app}>
      <Header />

      <main className={styles.main}>
        <section className={styles.filters}>
          <DeviceFilter value={deviceId} onChange={setDeviceId} devices={DEVICES} />
          <DateRangePicker
            startDate={startDate}
            endDate={endDate}
            onChange={(start, end) => {
              setStartDate(start);
              setEndDate(end);
            }}
          />
          <div className={styles.intervalFilter}>
            <label className={styles.label}>Interval</label>
            <select
              className={styles.select}
              value={interval}
              onChange={(e) => setInterval(e.target.value as 'hour' | 'day' | 'week')}
            >
              <option value="hour">Hour</option>
              <option value="day">Day</option>
              <option value="week">Week</option>
            </select>
          </div>
        </section>

        {error && (
          <div className={styles.error}>
            <p>{error}</p>
            <button onClick={refetch}>Retry</button>
          </div>
        )}

        <StatsPanel stats={loading ? null : stats} />

        {loading ? (
          <div className={styles.loading}>Loading data...</div>
        ) : (
          <section className={styles.charts}>
            <TimeSeriesChart
              data={timeseries}
              dataKey="avg_temperature"
              color="#ef4444"
              label="Temperature"
              unit="°C"
              interval={interval}
            />
            <TimeSeriesChart
              data={timeseries}
              dataKey="avg_humidity"
              color="#3b82f6"
              label="Humidity"
              unit="%"
              interval={interval}
            />
          </section>
        )}

        {!loading && <DataTable data={timeseries} device_id={deviceId || undefined} />}
      </main>
    </div>
  );
}
