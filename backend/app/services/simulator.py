import random
from datetime import datetime, timedelta

from app.models.schemas import MeasurementCreate


class SimulatorService:
    def __init__(
        self,
        temp_range: tuple[float, float] = (10.0, 40.0),
        humidity_range: tuple[float, float] = (20.0, 90.0),
    ):
        self.temp_range = temp_range
        self.humidity_range = humidity_range

    def generate(
        self,
        device_id: str | None = None,
        base_timestamp: datetime | None = None,
    ) -> MeasurementCreate:
        temp = self._clamp(self._normal_random(*self.temp_range), *self.temp_range)
        humidity = self._clamp(self._normal_random(*self.humidity_range), *self.humidity_range)

        timestamp = base_timestamp or datetime.utcnow()

        return MeasurementCreate(
            timestamp=timestamp,
            temperature=round(temp, 2),
            humidity=round(humidity, 2),
            device_id=device_id,
        )

    @staticmethod
    def _clamp(value: float, low: float, high: float) -> float:
        return max(low, min(high, value))

    def _normal_random(self, low: float, high: float) -> float:
        midpoint = (low + high) / 2
        spread = (high - low) / 6
        return random.gauss(midpoint, spread)

    def generate_batch(
        self,
        count: int,
        device_id: str | None = None,
        interval_seconds: int = 60,
        start_time: datetime | None = None,
    ) -> list[MeasurementCreate]:
        base_time = start_time or datetime.utcnow()
        measurements = []

        for i in range(count):
            timestamp = base_time - timedelta(seconds=interval_seconds * i)
            measurement = self.generate(device_id=device_id, base_timestamp=timestamp)
            measurements.append(measurement)

        return measurements
