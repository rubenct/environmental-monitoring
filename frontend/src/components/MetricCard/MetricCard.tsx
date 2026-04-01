import styles from './MetricCard.module.css';

interface MetricCardProps {
  label: string;
  value: number | null;
  unit: string;
  min?: number | null;
  max?: number | null;
}

export function MetricCard({ label, value, unit, min, max }: MetricCardProps) {
  return (
    <div className={styles.card}>
      <div className={styles.label}>{label}</div>
      <div className={styles.value}>
        {value !== null ? value.toFixed(1) : '—'}
        <span className={styles.unit}>{unit}</span>
      </div>
      <div className={styles.stats}>
        <span>Min: {min !== null && min !== undefined ? min.toFixed(1) : '—'}</span>
        <span>Max: {max !== null && max !== undefined ? max.toFixed(1) : '—'}</span>
      </div>
    </div>
  );
}
