import type { TimeseriesBucket } from '../../types';
import styles from './DataTable.module.css';

interface DataTableProps {
  data: TimeseriesBucket[];
  device_id?: string;
}

export function DataTable({ data, device_id }: DataTableProps) {
  if (data.length === 0) {
    return (
      <div className={styles.container}>
        <h3 className={styles.title}>Data Table</h3>
        <p className={styles.empty}>No data available for the selected range</p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Data Table</h3>
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Time</th>
              <th>Temperature</th>
              <th>Humidity</th>
              <th>Sensor</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>{row.timestamp}</td>
                <td>{row.avg_temperature.toFixed(2)} °C</td>
                <td>{row.avg_humidity.toFixed(2)} %</td>
                <td>{device_id || 'All'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
