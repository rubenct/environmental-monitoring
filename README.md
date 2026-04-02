# Environmental Monitoring System

A real-time environmental monitoring dashboard for collecting, storing, and visualizing temperature and humidity data from multiple sensors.

![Dashboard Preview](docs/dashboard-preview.png)

## Features

- **Real-time Data Visualization** - Interactive charts for temperature and humidity
- **Multi-Sensor Support** - Track multiple sensors simultaneously
- **Flexible Time Filtering** - View data by hour, day, or week
- **Statistical Analysis** - Average, minimum, and maximum values
- **Responsive Dashboard** - Works on desktop and mobile
- **Docker-Ready** - Full containerized deployment

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│                   Port: 5173 (dev) / 80 (prod)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                        │
│                        Port: 8000                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Routes     │→ │  Services    │→ │  Repository Pattern   │  │
│  └──────────────┘  └──────────────┘  └──────────┬───────────┘  │
│                                                 │              │
└─────────────────────────────────────────────────┼──────────────┘
                                                  │ SQL
                                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database (PostgreSQL)                        │
│                          Port: 5432                             │
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Backend

| Technology     | Version | Purpose                |
| -------------- | ------- | ---------------------- |
| **Python**     | 3.11+   | Core language          |
| **FastAPI**    | 0.109+  | REST API framework     |
| **SQLAlchemy** | 2.0+    | ORM with async support |
| **Pydantic**   | 2.5+    | Data validation        |
| **PostgreSQL** | 16+     | Relational database    |
| **Uvicorn**    | 0.27+   | ASGI server            |

### Frontend

| Technology      | Version | Purpose            |
| --------------- | ------- | ------------------ |
| **React**       | 18+     | UI framework       |
| **TypeScript**  | 5+      | Type safety        |
| **Vite**        | 5+      | Build tool         |
| **Recharts**    | 2.12+   | Data visualization |
| **date-fns**    | 3+      | Date manipulation  |
| **CSS Modules** | -       | Scoped styling     |

### Infrastructure

| Technology         | Purpose                       |
| ------------------ | ----------------------------- |
| **Docker**         | Containerization              |
| **Docker Compose** | Multi-container orchestration |
| **Nginx**          | Reverse proxy for production  |

## Project Structure

```
environmental-monitoring-system/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes and dependencies
│   │   ├── db/            # Database layer
│   │   ├── models/        # SQLAlchemy & Pydantic models
│   │   ├── services/      # Business logic
│   │   ├── main.py        # FastAPI application
│   │   └── config.py      # Settings
│   ├── tests/             # Unit & integration tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── types/         # TypeScript interfaces
│   │   ├── App.tsx        # Main application
│   │   └── main.tsx       # Entry point
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Docker & Docker Compose

### Run with Docker

```bash
# Clone the repository
git clone <repository-url>
cd environmental-monitoring-system

# Start all services (PostgreSQL, Backend, Frontend)
docker compose up -d

# Wait for services to be ready (~30 seconds)
sleep 30

# Seed the database with sample data (first time only)
docker exec environmental-monitoring-system-backend-1 python /app/seed.py

# View logs
docker compose logs -f

# Stop services
docker compose down
```

**Access:**

- **Dashboard**: <http://localhost:5173>
- **API Docs**: <http://localhost:8000/docs>
- **PostgreSQL**: localhost:5432

## API Endpoints

| Method | Endpoint                   | Description                     |
| ------ | -------------------------- | ------------------------------- |
| `POST` | `/measurements`            | Create a new measurement        |
| `GET`  | `/measurements`            | List measurements with filters  |
| `GET`  | `/measurements/stats`      | Get aggregated statistics       |
| `GET`  | `/measurements/timeseries` | Get time-series data for charts |
| `GET`  | `/health`                  | Health check                    |

### Example Requests

**Create Measurement:**

```bash
curl -X POST http://localhost:8000/measurements \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T10:30:00Z",
    "temperature": 23.5,
    "humidity": 65.0,
    "device_id": "sensor-01"
  }'
```

**Get Statistics:**

```bash
curl "http://localhost:8000/measurements/stats?start=2024-01-01T00:00:00Z&end=2024-01-07T23:59:59Z&device_id=sensor-01"
```

**Get Time-Series Data:**

```bash
curl "http://localhost:8000/measurements/timeseries?interval=hour&start=2024-01-01T00:00:00Z"
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Configuration

### Environment Variables

The application uses environment-specific configuration files:

#### Backend Configuration Files

| File           | Purpose                         | GitTracked |
| -------------- | ------------------------------- | ---------- |
| `.env.example` | Template for local development  | ✅ Yes     |
| `.env.local`   | Local development overrides     | ❌ No      |
| `.env.docker`  | Docker/Production configuration | ✅ Yes     |

#### Quick Setup

**For Local Development:**

```bash
cd backend
cp .env.example .env.local
# Edit .env.local if needed (defaults work for SQLite)
```

**For Docker Deployment:**

```bash
# Edit backend/.env.docker with production credentials
# docker-compose reads this automatically
```

#### Environment Variables Reference

**Backend (`backend/.env.local` or `backend/.env.docker`):**

```env
# Database connection
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
# Or for local: sqlite+aiosqlite:///./env_monitoring.db

# Server
HOST=0.0.0.0
PORT=8000
```

**Frontend (`frontend/.env`):**

```env
VITE_API_BASE_URL=http://localhost:8000
# Or for production: https://api.yourdomain.com
```

### Docker Environment Variables

In `docker-compose.yml`, the following variables can be overridden:

| Variable            | Default         | Description         |
| ------------------- | --------------- | ------------------- |
| `POSTGRES_USER`     | `envuser`       | PostgreSQL username |
| `POSTGRES_PASSWORD` | `changeme`      | PostgreSQL password |
| `POSTGRES_DB`       | `envmonitoring` | Database name       |

**Important:** For production, set these via environment or a secrets manager:

```bash
export POSTGRES_PASSWORD=your-secure-password
docker compose up -d
```

### Database Indexes

The system includes optimized indexes for common queries:

```sql
-- Primary key
measurements_pkey (id)

-- Filter by device
ix_measurements_device_id (device_id)

-- Filter by timestamp
ix_measurements_timestamp (timestamp)

-- Dashboard queries (time + device)
idx_timestamp_device (timestamp, device_id)
```

## Dashboard Features

### Filters

- **Device Filter** - Select specific sensor or view all
- **Date Range** - Custom time window selection
- **Interval** - Hour / Day / Week grouping

### Visualizations

- **Temperature Chart** - Line chart with real-time updates
- **Humidity Chart** - Line chart with real-time updates
- **Stats Cards** - Average, Min, Max values
- **Data Table** - Detailed measurement records

## Security Considerations

- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy ORM
- Environment-based configuration (no hardcoded secrets)
- CORS configuration ready for production

## Production Readiness

This setup is designed for **portfolio demonstration and development**. For production deployment, consider:

### Required Changes

| Area                   | Current                      | Production Requirement           |
| ---------------------- | ---------------------------- | -------------------------------- |
| **Secrets**            | Plain text in docker-compose | AWS Secrets Manager, Vault, etc. |
| **SSL/TLS**            | None                         | Let's Encrypt + Nginx            |
| **Connection Pooling** | None                         | PgBouncer or RDS Proxy           |
| **Authentication**     | None                         | JWT, OAuth2, or API Keys         |
| **Rate Limiting**      | None                         | Nginx limit_req or API Gateway   |
| **Monitoring**         | None                         | Prometheus + Grafana             |
| **Logging**            | Print statements             | Structured logging (JSON)        |

### Recommended Architecture for Production

```
                    ┌─────────────┐
                    │   Cloudflare│
                    │  (WAF + SSL)│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Load Balancer│
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │Backend 1│      │Backend 2│      │Backend 3│
    │(FastAPI)│      │(FastAPI)│      │(FastAPI)│
    └────┬────┘      └────┬────┘      └────┬────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼──────┐
                    │  PgBouncer   │
                    │(Connection  │
                    │   Pooling)  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  PostgreSQL │
                    │    (RDS)   │
                    └─────────────┘
```

## Performance Optimizations

- **Async I/O** - Non-blocking database operations
- **Compound Indexes** - Optimized for time-range queries
- **Connection Pooling** - Efficient database connections
- **Frontend Caching** - React hook with debouncing ready

## License

MIT License

## Author

Ruben Cariño

## Acknowledgments

- FastAPI for the excellent async API framework
- PostgreSQL for reliable data storage
- Recharts for beautiful React charts
- Vite for lightning-fast development experience
