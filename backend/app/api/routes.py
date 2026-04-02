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

# Valid values for interval/group_by parameters
VALID_INTERVALS = {"hour", "day", "week"}


def validate_interval(value: str, param_name: str = "interval") -> str:
    """Validate interval parameter. (DRY principle)"""
    if value not in VALID_INTERVALS:
        valid = ", ".join(sorted(VALID_INTERVALS))
        raise HTTPException(400, detail=f"{param_name} must be {valid}")
    return value


def validate_date_range(start: Optional[datetime], end: Optional[datetime]) -> None:
    """Validate that start is before end."""
    if start and end and end < start:
        raise HTTPException(400, detail="end must be after start")


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
    validate_date_range(start, end)

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
    if group_by:
        validate_interval(group_by, "group_by")

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
    interval = validate_interval(interval)

    service = MeasurementService(session)
    return await service.get_timeseries(
        start=start,
        end=end,
        device_id=device_id,
        interval=interval,
    )
