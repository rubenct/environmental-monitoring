import styles from './DeviceFilter.module.css';

interface DeviceFilterProps {
  value: string;
  onChange: (device_id: string) => void;
  devices: string[];
}

export function DeviceFilter({ value, onChange, devices }: DeviceFilterProps) {
  return (
    <div className={styles.filter}>
      <label className={styles.label} htmlFor="device-filter">Device</label>
      <select
        id="device-filter"
        className={styles.select}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">All Devices</option>
        {devices.map((device) => (
          <option key={device} value={device}>
            {device}
          </option>
        ))}
      </select>
    </div>
  );
}
