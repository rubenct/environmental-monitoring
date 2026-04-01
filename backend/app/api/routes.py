from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.api.deps import SessionDep
from app.models.schemas import (
    MeasurementCreate,
    MeasurementResponse,
    QueryParams,
    StatsResponse,
    TimeseriesBucket,
)
from app.services.measurement import MeasurementService

router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.post("", response_model=MeasurementResponse, status_code=201)
async def create_measurement(data: MeasurementCreate, session: SessionDep) -> MeasurementResponse:
    service = MeasurementService(session)
    return await service.create(data)


@router.get("", response_model=list[MeasurementResponse])
async def get_measurements(
    session: SessionDep,
    start: Optional[datetime] = Query(None, description="Start of time range (ISO 8601)"),
    end: Optional[datetime] = Query(None, description="End of time range (ISO 8601)"),
    device_id: Optional[str] = Query(None, description="Filter by device ID"),
    limit: int = Query(100, ge=1, le=1000, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
) -> list[MeasurementResponse]:
    if start and end and end < start:
        raise HTTPException(status_code=400, detail="end must be after start")

    params = QueryParams(
        start=start,
        end=end,
        device_id=device_id,
        limit=limit,
        offset=offset,
    )
    service = MeasurementService(session)
    return await service.query(params)


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    session: SessionDep,
    start: Optional[datetime] = Query(None, description="Start of time range"),
    end: Optional[datetime] = Query(None, description="End of time range"),
    device_id: Optional[str] = Query(None, description="Filter by device ID"),
    group_by: Optional[str] = Query(None, description="Group by: hour, day, week"),
) -> StatsResponse:
    if group_by and group_by not in ("hour", "day", "week"):
        raise HTTPException(status_code=400, detail="group_by must be hour, day, or week")

    service = MeasurementService(session)
    return await service.get_stats(
        start=start,
        end=end,
        device_id=device_id,
        group_by=group_by,
    )


@router.get("/timeseries", response_model=list[TimeseriesBucket])
async def get_timeseries(
    session: SessionDep,
    start: Optional[datetime] = Query(None, description="Start of time range"),
    end: Optional[datetime] = Query(None, description="End of time range"),
    device_id: Optional[str] = Query(None, description="Filter by device ID"),
    interval: str = Query("hour", description="Interval: hour, day, week"),
) -> list[TimeseriesBucket]:
    if interval not in ("hour", "day", "week"):
        raise HTTPException(status_code=400, detail="interval must be hour, day, or week")

    service = MeasurementService(session)
    return await service.get_timeseries(
        start=start,
        end=end,
        device_id=device_id,
        interval=interval,
    )
