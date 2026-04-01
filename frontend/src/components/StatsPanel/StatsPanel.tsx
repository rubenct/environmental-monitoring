import { MetricCard } from '../MetricCard/MetricCard';
import type { Stats } from '../../types';
import styles from './StatsPanel.module.css';

interface StatsPanelProps {
  stats: Stats | null;
}

export function StatsPanel({ stats }: StatsPanelProps) {
  if (!stats) {
    return (
      <div className={styles.panel}>
        <div className={styles.loading}>Loading stats...</div>
      </div>
    );
  }

  return (
    <div className={styles.panel}>
      <MetricCard
        label="Temperature"
        value={stats.temperature.avg}
        unit="°C"
        min={stats.temperature.min}
        max={stats.temperature.max}
      />
      <MetricCard
        label="Humidity"
        value={stats.humidity.avg}
        unit="%"
        min={stats.humidity.min}
        max={stats.humidity.max}
      />
    </div>
  );
}
