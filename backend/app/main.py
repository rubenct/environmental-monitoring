import logging
import random
import sys
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.database import init_db, async_session_maker
from app.models.db_models import Measurement
from app.config import settings


# Configure structured logging
def setup_logging():
    """Configure JSON logging for production."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if settings.is_production:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


setup_logging()
logger = logging.getLogger(__name__)


async def seed_database_if_empty():
    """Seed database with sample data if it's empty."""
    async with async_session_maker() as session:
        from sqlalchemy import select, func
        result = await session.execute(select(func.count(Measurement.id)))
        count = result.scalar() or 0
        
        if count > 0:
            logger.info(f"Database already has {count} measurements, skipping seed")
            return
        
        logger.info("Database is empty, seeding with sample data...")
        
        # Temperature pattern by hour (cooler at night, warmer midday)
        temps_by_hour = [15, 14, 14, 14, 14, 15, 17, 19, 21, 23, 24, 25, 26, 26, 26, 25, 24, 22, 20, 18, 17, 16, 16, 15]
        hums_by_hour = [85, 87, 87, 87, 87, 85, 80, 75, 70, 65, 62, 60, 58, 58, 58, 60, 62, 67, 72, 77, 80, 82, 84, 85]
        sensors = ["sensor-01", "sensor-02", "sensor-03"]
        sensor_offset = {"sensor-01": 0, "sensor-02": 2, "sensor-03": -1}
        
        measurements = []
        now = datetime.utcnow()
        
        # Generate 7 days of data, every 2 hours, 3 sensors
        for day_offset in range(7, -1, -1):
            for hour in range(0, 24, 2):
                # Skip future hours for today
                if day_offset == 0 and hour > now.hour:
                    continue
                
                timestamp = now - timedelta(days=day_offset, hours=now.hour - hour)
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
                    
                    measurements.append(Measurement(
                        timestamp=timestamp,
                        temperature=round(temp, 1),
                        humidity=round(hum, 1),
                        device_id=sensor_id
                    ))
        
        session.add_all(measurements)
        await session.commit()
        logger.info(f"Seeded database with {len(measurements)} measurements")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager."""
    logger.info(
        "Starting Environmental Monitoring API",
        extra={
            "environment": settings.environment,
            "is_production": settings.is_production
        }
    )
    await init_db()
    logger.info("Database initialized successfully")
    
    # Seed data if empty
    await seed_database_if_empty()
    
    yield
    logger.info("Shutting down Environmental Monitoring API")


app = FastAPI(
    title="Environmental Monitoring API",
    description="Real-time environmental monitoring system API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins in production for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0"
    }
