import asyncio
from datetime import datetime
from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.models.db_models import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_db: AsyncSession) -> AsyncIterator[AsyncClient]:
    from app.db.database import get_session

    async def override_get_session():
        yield test_db

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def sample_measurement_data() -> dict:
    return {
        "timestamp": "2024-01-15T10:30:00Z",
        "temperature": 22.5,
        "humidity": 65.0,
        "device_id": "sensor-01",
    }


@pytest.fixture
def sample_measurements_batch() -> list[dict]:
    base_time = datetime(2024, 1, 15, 10, 0, 0)
    return [
        {
            "timestamp": (base_time.replace(hour=h)).isoformat() + "Z",
            "temperature": 20.0 + h * 0.5,
            "humidity": 60.0 + h * 2,
            "device_id": "sensor-01",
        }
        for h in range(5)
    ]
