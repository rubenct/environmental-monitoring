import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.database import init_db
from app.config import settings


# Configure structured logging
def setup_logging():
    """Configure JSON logging for production."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if settings.is_production:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            handlers=[logging.StreamHandler(sys.stdout)]
        )

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager."""
    logger.info(
        "Starting Environmental Monitoring API",
        extra={
            "environment": settings.environment,
            "is_production": settings.is_production
        }
    )
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down Environmental Monitoring API")


app = FastAPI(
    title="Environmental Monitoring API",
    description="Real-time environmental monitoring system API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins in production for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0"
    }
