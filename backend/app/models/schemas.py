from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MeasurementCreate(BaseModel):
    timestamp: datetime
    temperature: float = Field(ge=-100, le=100)
    humidity: float = Field(ge=0, le=100)
    device_id: Optional[str] = Field(default=None, max_length=64)


class MeasurementResponse(BaseModel):
    id: UUID
    timestamp: datetime
    temperature: float
    humidity: float
    device_id: Optional[str]

    model_config = {"from_attributes": True}


class AggregatedStats(BaseModel):
    avg: Optional[float]
    min: Optional[float]
    max: Optional[float]


class StatsResponse(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]
    device_id: Optional[str]
    temperature: AggregatedStats
    humidity: AggregatedStats


class TimeseriesBucket(BaseModel):
    timestamp: datetime
    avg_temperature: float
    avg_humidity: float
    count: int


class QueryParams(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    device_id: Optional[str] = None
    limit: int = Field(default=100, le=1000)
    offset: int = Field(default=0, ge=0)


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    errors: Optional[list] = None
