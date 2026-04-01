from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import MeasurementRepository
from app.models.schemas import (
    MeasurementCreate,
    MeasurementResponse,
    QueryParams,
    StatsResponse,
    TimeseriesBucket,
)


class MeasurementService:
    def __init__(self, session: AsyncSession):
        self.repository = MeasurementRepository(session)

    async def create(self, data: MeasurementCreate) -> MeasurementResponse:
        measurement = await self.repository.create(
            timestamp=data.timestamp,
            temperature=data.temperature,
            humidity=data.humidity,
            device_id=data.device_id,
        )
        return MeasurementResponse.model_validate(measurement)

    async def query(self, params: QueryParams) -> list[MeasurementResponse]:
        measurements = await self.repository.query(
            start=params.start,
            end=params.end,
            device_id=params.device_id,
            limit=params.limit,
            offset=params.offset,
        )
        return [MeasurementResponse.model_validate(m) for m in measurements]

    async def get_stats(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        device_id: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> StatsResponse:
        stats = await self.repository.get_stats(
            start=start,
            end=end,
            device_id=device_id,
            group_by=group_by,
        )
        return StatsResponse(
            start=start,
            end=end,
            device_id=device_id,
            temperature=stats["temperature"],
            humidity=stats["humidity"],
        )

    async def get_timeseries(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        device_id: Optional[str] = None,
        interval: str = "hour",
    ) -> list[TimeseriesBucket]:
        buckets = await self.repository.get_timeseries(
            start=start,
            end=end,
            device_id=device_id,
            interval=interval,
        )
        result = []
        for b in buckets:
            ts = b["timestamp"]
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            elif ts is None:
                continue
            result.append(TimeseriesBucket(
                timestamp=ts,
                avg_temperature=b["avg_temperature"],
                avg_humidity=b["avg_humidity"],
                count=b["count"],
            ))
        return result
