import pytest
from httpx import AsyncClient


class TestMeasurementIngestion:
    @pytest.mark.asyncio
    async def test_create_measurement(self, client: AsyncClient, sample_measurement_data: dict):
        response = await client.post("/measurements", json=sample_measurement_data)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["temperature"] == sample_measurement_data["temperature"]
        assert data["humidity"] == sample_measurement_data["humidity"]
        assert data["device_id"] == sample_measurement_data["device_id"]

    @pytest.mark.asyncio
    async def test_create_measurement_without_device_id(self, client: AsyncClient):
        data = {
            "timestamp": "2024-01-15T10:30:00Z",
            "temperature": 22.5,
            "humidity": 65.0,
        }
        response = await client.post("/measurements", json=data)

        assert response.status_code == 201
        assert response.json()["device_id"] is None

    @pytest.mark.asyncio
    async def test_create_measurement_invalid_temperature(self, client: AsyncClient):
        data = {
            "timestamp": "2024-01-15T10:30:00Z",
            "temperature": 150.0,
            "humidity": 65.0,
        }
        response = await client.post("/measurements", json=data)

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_measurement_missing_field(self, client: AsyncClient):
        data = {
            "timestamp": "2024-01-15T10:30:00Z",
            "temperature": 22.5,
        }
        response = await client.post("/measurements", json=data)

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_measurement_invalid_timestamp(self, client: AsyncClient):
        data = {
            "timestamp": "not-a-timestamp",
            "temperature": 22.5,
            "humidity": 65.0,
        }
        response = await client.post("/measurements", json=data)

        assert response.status_code == 422


class TestMeasurementQuery:
    @pytest.mark.asyncio
    async def test_get_measurements_empty(self, client: AsyncClient):
        response = await client.get("/measurements")

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_measurements_with_data(
        self, client: AsyncClient, sample_measurements_batch: list[dict]
    ):
        for m in sample_measurements_batch:
            await client.post("/measurements", json=m)

        response = await client.get("/measurements")

        assert response.status_code == 200
        assert len(response.json()) == 5

    @pytest.mark.asyncio
    async def test_get_measurements_by_device(
        self, client: AsyncClient, sample_measurements_batch: list[dict]
    ):
        for m in sample_measurements_batch:
            await client.post("/measurements", json=m)

        response = await client.get("/measurements", params={"device_id": "sensor-01"})

        assert response.status_code == 200
        assert all(m["device_id"] == "sensor-01" for m in response.json())

    @pytest.mark.asyncio
    async def test_get_measurements_by_time_range(
        self, client: AsyncClient, sample_measurements_batch: list[dict]
    ):
        for m in sample_measurements_batch:
            await client.post("/measurements", json=m)

        response = await client.get(
            "/measurements",
            params={
                "start": "2024-01-15T10:00:00Z",
                "end": "2024-01-15T12:00:00Z",
            },
        )

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_measurements_invalid_range(self, client: AsyncClient):
        response = await client.get(
            "/measurements",
            params={
                "start": "2024-01-15T12:00:00Z",
                "end": "2024-01-15T10:00:00Z",
            },
        )

        assert response.status_code == 400


class TestMeasurementStats:
    @pytest.mark.asyncio
    async def test_get_stats(self, client: AsyncClient, sample_measurements_batch: list[dict]):
        for m in sample_measurements_batch:
            await client.post("/measurements", json=m)

        response = await client.get("/measurements/stats")

        assert response.status_code == 200
        data = response.json()
        assert "temperature" in data
        assert "humidity" in data
        assert "avg" in data["temperature"]
        assert "min" in data["temperature"]
        assert "max" in data["temperature"]

    @pytest.mark.asyncio
    async def test_get_stats_with_device_filter(
        self, client: AsyncClient, sample_measurements_batch: list[dict]
    ):
        for m in sample_measurements_batch:
            await client.post("/measurements", json=m)

        response = await client.get("/measurements/stats", params={"device_id": "sensor-01"})

        assert response.status_code == 200
        assert response.json()["device_id"] == "sensor-01"

    @pytest.mark.asyncio
    async def test_get_stats_invalid_group_by(self, client: AsyncClient):
        response = await client.get("/measurements/stats", params={"group_by": "invalid"})

        assert response.status_code == 400


class TestTimeseries:
    @pytest.mark.asyncio
    async def test_get_timeseries(self, client: AsyncClient, sample_measurements_batch: list[dict]):
        for m in sample_measurements_batch:
            await client.post("/measurements", json=m)

        response = await client.get("/measurements/timeseries")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_timeseries_hourly(
        self, client: AsyncClient, sample_measurements_batch: list[dict]
    ):
        for m in sample_measurements_batch:
            await client.post("/measurements", json=m)

        response = await client.get("/measurements/timeseries", params={"interval": "hour"})

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_timeseries_invalid_interval(self, client: AsyncClient):
        response = await client.get("/measurements/timeseries", params={"interval": "invalid"})

        assert response.status_code == 400


class TestHealthCheck:
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
