import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.routes import router
from app.db.database import init_db
from app.config import settings


# Configure structured logging
def setup_logging():
    """Configure JSON logging for production."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if settings.is_production:
        # Use JSON logging in production
        try:
            from pythonjsonlogger import jsonlogger
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(jsonlogger.JsonFormatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s"
            ))
            logging.root.handlers = [handler]
            logging.root.setLevel(logging.INFO)
        except ImportError:
            # Fallback to standard logging if json logger not available
            logging.basicConfig(
                level=logging.INFO,
                format=log_format,
                handlers=[logging.StreamHandler(sys.stdout)]
            )
    else:
        # Development: human-readable logs
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


# Rate limiter
limiter = Limiter(key_func=get_remote_address)


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

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if not settings.is_production else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client_ip": get_remote_address(request)
        }
    )
    response = await call_next(request)
    return response


# Global rate limit: 100 requests per minute
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all requests."""
    # Skip rate limiting for health checks
    if request.url.path == "/health":
        return await call_next(request)
    
    # Rate limit: 100/min, burst of 20
    try:
        await limiter.check(
            request, 
            f"{settings.rate_limit_requests}_per_minute"
        )
    except RateLimitExceeded:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )
    
    return await call_next(request)


app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0"
    }
