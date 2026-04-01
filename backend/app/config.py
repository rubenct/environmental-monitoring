from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Production priority (Railway, Docker):
    - DATABASE_URL: Provided by Railway's PostgreSQL or custom env var
    - PORT: Provided by Railway (the port to listen on)
    - ENVIRONMENT: Set to 'production' in production deployments
    
    Development priority:
    - .env.local (gitignored, local overrides)
    - .env.example (defaults for dev)
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Database - Railway provides DATABASE_URL, fallback to SQLite for local dev
    database_url: str = os.environ.get(
        "DATABASE_URL", 
        "sqlite+aiosqlite:///./env_monitoring.db"
    )
    
    # Server - Railway provides PORT, default for local dev
    host: str = "0.0.0.0"
    port: int = int(os.environ.get("PORT", "8000"))
    
    # Environment
    environment: str = os.environ.get("ENVIRONMENT", "development")
    
    # CORS - restrict in production
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    
    # Rate limiting
    rate_limit_requests: int = 100  # per minute
    rate_limit_burst: int = 20
    
    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ("production", "prod")


settings = Settings()
