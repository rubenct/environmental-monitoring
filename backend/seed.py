#!/usr/bin/env python3
"""Seed the database with sample data for testing."""

import asyncio
from datetime import datetime, timedelta
import random

from app.db.database import async_session_maker, init_db
from app.db.repositories import MeasurementRepository


async def seed_data():
    await init_db()
    
    async with async_session_maker() as session:
        repo = MeasurementRepository(session)
        base = datetime.utcnow()
        
        # Generate 7 weeks of data for each sensor
        for device in ['sensor-01', 'sensor-02', 'sensor-03']:
            print(f"Seeding data for {device}...")
            
            for week in range(7):
                for day in range(7):
                    for hour in range(24):
                        timestamp = base - timedelta(
                            weeks=week, 
                            days=day, 
                            hours=hour
                        )
                        
                        # Generate realistic values
                        base_temp = random.uniform(18, 30)
                        base_humidity = random.uniform(40, 70)
                        
                        temp = base_temp + random.uniform(-3, 3)
                        humidity = base_humidity + random.uniform(-10, 10)
                        
                        await repo.create(
                            timestamp=timestamp,
                            temperature=round(temp, 2),
                            humidity=round(humidity, 2),
                            device_id=device,
                        )
            
            print(f"Done: {device}")
        
        print(f"Total measurements seeded: 3 sensors × 7 weeks × 7 days × 24 hours = ~3528")


if __name__ == "__main__":
    asyncio.run(seed_data())
