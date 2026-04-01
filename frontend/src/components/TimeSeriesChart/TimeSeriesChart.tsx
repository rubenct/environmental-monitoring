import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { format, parseISO, getWeek } from 'date-fns';
import type { TimeseriesBucket } from '../../types';
import styles from './TimeSeriesChart.module.css';

interface TimeSeriesChartProps {
  data: TimeseriesBucket[];
  dataKey: 'avg_temperature' | 'avg_humidity';
  color: string;
  label: string;
  unit: string;
  interval: 'hour' | 'day' | 'week';
}

interface FormattedData {
  timestamp: string;
  avg_temperature: number;
  avg_humidity: number;
  count: number;
  time: string;
  dateLabel: string;
  fullTime: string;
}

function CustomTick(props: { x?: number; y?: number; payload?: { value: string; index: number }; interval: string; formattedData: FormattedData[] }) {
  const { x, y, payload, interval, formattedData } = props;
  if (!payload || x === undefined || y === undefined) return null;
  
  const item = formattedData[payload.index];
  if (!item) return null;

  if (interval === 'hour') {
    return (
      <g transform={`translate(${x},${y})`}>
        <text x={0} y={0} textAnchor="middle" dominantBaseline="auto" style={{ fontSize: 12, fill: '#64748b' }}>
          <tspan x={0} dy="0.8em">{item.time}</tspan>
          <tspan x={0} dy="1.2em">{item.dateLabel}</tspan>
        </text>
      </g>
    );
  }

  return (
    <text x={x} y={y + 15} textAnchor="middle" style={{ fontSize: 12, fill: '#64748b' }}>
      {payload.value}
    </text>
  );
}

export function TimeSeriesChart({ data, dataKey, color, label, unit, interval }: TimeSeriesChartProps) {
  const formatTime = (timestamp: string): string => {
    const date = parseISO(timestamp);
    switch (interval) {
      case 'hour':
        return format(date, 'HH:mm');
      case 'day':
        return format(date, 'MMM d');
      case 'week':
        return `Week ${getWeek(date)}`;
      default:
        return format(date, 'HH:mm');
    }
  };

  const formatDateForHour = (timestamp: string): string => {
    const date = parseISO(timestamp);
    return format(date, 'MMM d');
  };

  const formattedData: FormattedData[] = data.map((d) => ({
    ...d,
    time: formatTime(d.timestamp),
    dateLabel: formatDateForHour(d.timestamp),
    fullTime: format(parseISO(d.timestamp), 'PPp'),
  }));

  return (
    <div className={styles.chartContainer}>
      <h3 className={styles.chartTitle}>{label}</h3>
      <div className={styles.chart}>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={formattedData} margin={{ top: 10, right: 30, left: 0, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="time" 
              stroke="#64748b" 
              tickCount={interval === 'day' ? 7 : undefined}
              tickLine={false}
              tick={<CustomTick interval={interval} formattedData={formattedData} />}
            />
            <YAxis tick={{ fontSize: 12 }} stroke="#64748b" unit={unit} domain={['auto', 'auto']} />
            <Tooltip
              contentStyle={{ borderRadius: '0.5rem', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
              formatter={(value: number) => [`${value.toFixed(2)} ${unit}`, label]}
              labelFormatter={(_, payload) => payload?.[0]?.payload?.fullTime || ''}
            />
            <Line
              type="monotone"
              dataKey={dataKey}
              stroke={color}
              strokeWidth={2}
              dot={{ fill: color, strokeWidth: 2, r: 3 }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
