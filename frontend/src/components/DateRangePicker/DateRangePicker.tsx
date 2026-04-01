import { format } from 'date-fns';
import styles from './DateRangePicker.module.css';

interface DateRangePickerProps {
  startDate: Date | null;
  endDate: Date | null;
  onChange: (start: Date | null, end: Date | null) => void;
}

function parseLocalDateTime(value: string): Date | null {
  if (!value) return null;
  const [date, time] = value.split('T');
  const [year, month, day] = date.split('-').map(Number);
  const [hour, minute] = time.split(':').map(Number);
  return new Date(year, month - 1, day, hour, minute, 0, 0);
}

export function DateRangePicker({ startDate, endDate, onChange }: DateRangePickerProps) {
  const handleStartChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    onChange(parseLocalDateTime(value), endDate);
  };

  const handleEndChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    onChange(startDate, parseLocalDateTime(value));
  };

  return (
    <div className={styles.picker}>
      <div className={styles.field}>
        <label className={styles.label} htmlFor="start-date">From</label>
        <input
          id="start-date"
          type="datetime-local"
          className={styles.input}
          value={startDate ? format(startDate, "yyyy-MM-dd'T'HH:mm") : ''}
          onChange={handleStartChange}
        />
      </div>
      <div className={styles.field}>
        <label className={styles.label} htmlFor="end-date">To</label>
        <input
          id="end-date"
          type="datetime-local"
          className={styles.input}
          value={endDate ? format(endDate, "yyyy-MM-dd'T'HH:mm") : ''}
          onChange={handleEndChange}
        />
      </div>
    </div>
  );
}
