import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MetricCard } from './MetricCard';

describe('MetricCard', () => {
  it('renders label and value', () => {
    render(<MetricCard label="Temperature" value={25.5} unit="°C" />);
    expect(screen.getByText('Temperature')).toBeDefined();
    expect(screen.getByText('25.5')).toBeDefined();
    expect(screen.getByText('°C')).toBeDefined();
  });

  it('renders min and max values', () => {
    render(<MetricCard label="Temperature" value={25.5} unit="°C" min={20.0} max={30.0} />);
    expect(screen.getByText(/Min:/)).toBeDefined();
    expect(screen.getByText(/Max:/)).toBeDefined();
  });

  it('renders dash for null value', () => {
    render(<MetricCard label="Temperature" value={null} unit="°C" />);
    expect(screen.getByText('—')).toBeDefined();
    expect(screen.getByText('°C')).toBeDefined();
  });
});
