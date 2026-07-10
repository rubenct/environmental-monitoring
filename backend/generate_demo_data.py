#!/usr/bin/env python3
"""
Generate SQLite database with realistic environmental data for portfolio demo.
Run this script to create env_monitoring.db with 7 days of data.
"""

import sqlite3
import random
from datetime import datetime, timedelta

def generate_data():
    """Generate 7 days of realistic environmental data with fixed dates."""
    
    # Fixed date range: January 1-7, 2024
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    
    # Temperature pattern by hour (cooler at night, warmer midday)
    temps_by_hour = [15, 14, 14, 14, 14, 15, 17, 19, 21, 23, 24, 25, 26, 26, 26, 25, 24, 22, 20, 18, 17, 16, 16, 15]
    hums_by_hour = [85, 87, 87, 87, 87, 85, 80, 75, 70, 65, 62, 60, 58, 58, 58, 60, 62, 67, 72, 77, 80, 82, 84, 85]
    
    sensors = ["sensor-01", "sensor-02", "sensor-03"]
    sensor_offset = {"sensor-01": 0, "sensor-02": 2, "sensor-03": -1}
    
    measurements = []
    
    # Generate 7 days of data, every 2 hours, 3 sensors
    for day_offset in range(7):
        for hour in range(0, 24, 2):
            timestamp = start_date + timedelta(days=day_offset, hours=hour)
            base_temp = temps_by_hour[hour]
            base_hum = hums_by_hour[hour]
            daily_var = random.randint(-2, 2)
            
            for sensor_id in sensors:
                offset = sensor_offset[sensor_id]
                temp = base_temp + offset + daily_var + random.uniform(-0.5, 0.5)
                hum = base_hum - offset * 2 - daily_var * 1.5 + random.uniform(-2, 2)
                
                # Clamp values
                temp = max(5, min(35, temp))
                hum = max(30, min(95, hum))
                
                measurements.append({
                    "timestamp": timestamp.isoformat(),
                    "temperature": round(temp, 1),
                    "humidity": round(hum, 1),
                    "device_id": sensor_id
                })
    
    return measurements

def create_database():
    """Create SQLite database with measurements table."""
    
    db_path = "env_monitoring.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            device_id TEXT
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON measurements(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_device_id ON measurements(device_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp_device ON measurements(timestamp, device_id)")
    
    # Generate and insert data
    print("Generating data...")
    measurements = generate_data()
    
    print(f"Inserting {len(measurements)} measurements...")
    for m in measurements:
        cursor.execute(
            "INSERT INTO measurements (id, timestamp, temperature, humidity, device_id) VALUES (?, ?, ?, ?, ?)",
            (
                f"{m['timestamp']}-{m['device_id']}",  # Simple ID
                m['timestamp'],
                m['temperature'],
                m['humidity'],
                m['device_id']
            )
        )
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM measurements")
    count = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(temperature), MIN(temperature), MAX(temperature) FROM measurements")
    temp_stats = cursor.fetchone()
    
    cursor.execute("SELECT AVG(humidity), MIN(humidity), MAX(humidity) FROM measurements")
    hum_stats = cursor.fetchone()
    
    conn.close()
    
    print(f"\n✅ Database created: {db_path}")
    print(f"   Total measurements: {count}")
    print(f"   Temperature: avg={temp_stats[0]:.1f}°C, min={temp_stats[1]:.1f}°C, max={temp_stats[2]:.1f}°C")
    print(f"   Humidity: avg={hum_stats[0]:.1f}%, min={hum_stats[1]:.1f}%, max={hum_stats[2]:.1f}%")

if __name__ == "__main__":
    create_database()
