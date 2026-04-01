from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = (
        # Compound index for time-range + device queries (most common dashboard query)
        Index('idx_timestamp_device', 'timestamp', 'device_id'),
        # Index for time-range queries across all devices
        Index('idx_timestamp', 'timestamp'),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    timestamp: Mapped[datetime] = mapped_column(index=True)
    temperature: Mapped[float]
    humidity: Mapped[float]
    device_id: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
