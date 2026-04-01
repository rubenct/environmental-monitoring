import pytest
from datetime import datetime

from app.models.schemas import MeasurementCreate
from app.services.simulator import SimulatorService


class TestSimulatorService:
    def test_generate_single_measurement(self):
        simulator = SimulatorService(
            temp_range=(10.0, 40.0),
            humidity_range=(20.0, 90.0),
        )

        measurement = simulator.generate(device_id="test-sensor")

        assert measurement.temperature >= 10.0
        assert measurement.temperature <= 40.0
        assert measurement.humidity >= 20.0
        assert measurement.humidity <= 90.0
        assert measurement.device_id == "test-sensor"
        assert measurement.timestamp is not None

    def test_generate_with_custom_ranges(self):
        simulator = SimulatorService(
            temp_range=(25.0, 30.0),
            humidity_range=(40.0, 50.0),
        )

        for _ in range(100):
            measurement = simulator.generate()
            assert 25.0 <= measurement.temperature <= 30.0
            assert 40.0 <= measurement.humidity <= 50.0

    def test_generate_batch(self):
        simulator = SimulatorService()

        batch = simulator.generate_batch(count=5, device_id="batch-sensor")

        assert len(batch) == 5
        assert all(m.device_id == "batch-sensor" for m in batch)

    def test_generate_batch_decreasing_timestamps(self):
        simulator = SimulatorService()
        start_time = datetime(2024, 1, 15, 12, 0, 0)

        batch = simulator.generate_batch(
            count=3,
            interval_seconds=60,
            start_time=start_time,
        )

        assert batch[0].timestamp == start_time
        assert batch[1].timestamp < batch[0].timestamp
        assert batch[2].timestamp < batch[1].timestamp

    def test_measurement_create_validation(self):
        data = MeasurementCreate(
            timestamp=datetime(2024, 1, 15),
            temperature=25.0,
            humidity=60.0,
            device_id="test",
        )
        assert data.temperature == 25.0
        assert data.humidity == 60.0

    def test_measurement_create_temperature_out_of_range(self):
        with pytest.raises(Exception):
            MeasurementCreate(
                timestamp=datetime(2024, 1, 15),
                temperature=150.0,
                humidity=60.0,
            )

    def test_measurement_create_humidity_out_of_range(self):
        with pytest.raises(Exception):
            MeasurementCreate(
                timestamp=datetime(2024, 1, 15),
                temperature=25.0,
                humidity=150.0,
            )
