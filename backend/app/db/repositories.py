from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import Measurement


class MeasurementRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        timestamp: datetime,
        temperature: float,
        humidity: float,
        device_id: Optional[str] = None,
    ) -> Measurement:
        measurement = Measurement(
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity,
            device_id=device_id,
        )
        self.session.add(measurement)
        await self.session.commit()
        await self.session.refresh(measurement)
        return measurement

    async def get_by_id(self, measurement_id: UUID) -> Optional[Measurement]:
        result = await self.session.execute(
            select(Measurement).where(Measurement.id == measurement_id)
        )
        return result.scalar_one_or_none()

    async def query(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        device_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Measurement]:
        query = select(Measurement)

        if start is not None:
            query = query.where(Measurement.timestamp >= start)
        if end is not None:
            query = query.where(Measurement.timestamp <= end)
        if device_id is not None:
            query = query.where(Measurement.device_id == device_id)

        query = query.order_by(Measurement.timestamp.desc())
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_stats(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        device_id: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> dict:
        query = select(
            func.avg(Measurement.temperature).label("avg_temp"),
            func.min(Measurement.temperature).label("min_temp"),
            func.max(Measurement.temperature).label("max_temp"),
            func.avg(Measurement.humidity).label("avg_humidity"),
            func.min(Measurement.humidity).label("min_humidity"),
            func.max(Measurement.humidity).label("max_humidity"),
        )

        if device_id is not None:
            query = query.where(Measurement.device_id == device_id)
        if start is not None:
            query = query.where(Measurement.timestamp >= start)
        if end is not None:
            query = query.where(Measurement.timestamp <= end)

        result = await self.session.execute(query)
        row = result.one()

        return {
            "temperature": {
                "avg": row.avg_temp,
                "min": row.min_temp,
                "max": row.max_temp,
            },
            "humidity": {
                "avg": row.avg_humidity,
                "min": row.min_humidity,
                "max": row.max_humidity,
            },
        }

    async def get_timeseries(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        device_id: Optional[str] = None,
        interval: str = "hour",
    ) -> list[dict]:
        query = select(Measurement)

        if device_id is not None:
            query = query.where(Measurement.device_id == device_id)
        if start is not None:
            query = query.where(Measurement.timestamp >= start)
        if end is not None:
            query = query.where(Measurement.timestamp <= end)

        query = query.order_by(Measurement.timestamp)

        result = await self.session.execute(query)
        measurements = result.scalars().all()

        buckets: dict[str, list[Measurement]] = {}
        for m in measurements:
            key = self._truncate_timestamp(m.timestamp, interval)
            if key not in buckets:
                buckets[key] = []
            buckets[key].append(m)

        return [
            {
                "timestamp": key,
                "avg_temperature": sum(x.temperature for x in bucket) / len(bucket),
                "avg_humidity": sum(x.humidity for x in bucket) / len(bucket),
                "count": len(bucket),
            }
            for key, bucket in sorted(buckets.items())
        ]

    def _truncate_timestamp(self, ts: datetime, interval: str) -> str:
        if interval == "hour":
            return ts.replace(minute=0, second=0, microsecond=0).isoformat()
        elif interval == "day":
            return ts.date().isoformat()
        else:
            week = ts.isocalendar()[1]
            return f"{ts.year}-W{week:02d}"
