# Environmental Monitoring System

A real-time environmental monitoring dashboard for collecting, storing, and visualizing temperature and humidity data from multiple sensors.

**Live Demo:** https://env-monitoring.vercel.app

**API:** https://alert-forgiveness-production.up.railway.app

**GitHub:** https://github.com/rubenct/environmental-monitoring

## Features

- **Real-time Data Visualization** - Interactive charts for temperature and humidity
- **Multi-Sensor Support** - Track multiple sensors simultaneously
- **Flexible Time Filtering** - View data by hour, day, or week
- **Statistical Analysis** - Average, minimum, and maximum values
- **Responsive Dashboard** - Works on desktop and mobile

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend (Vercel)                          │
│                   https://env-monitoring.vercel.app             │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API (Railway)                        │
│              https://alert-forgiveness-production.up.railway.app│
│                        Port: 8000                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Routes     │→ │  Services    │→ │  Repository Pattern   │  │
│  └──────────────┘  └──────────────┘  └──────────┬───────────┘  │
│                                                 │              │
└─────────────────────────────────────────────────┼──────────────┘
                                                  │ SQL
                                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database (Railway PostgreSQL)                  │
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

### Infrastructure

| Technology    | Purpose                |
| ------------- | --------------------- |
| **Railway**   | Backend hosting       |
| **Vercel**    | Frontend hosting      |
| **PostgreSQL**| Database (Railway)    |
| **Docker**    | Containerization      |

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

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or use SQLite for development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the dev server
npm run dev
```

### Run with Docker

```bash
# Start all services
docker compose up -d

# Seed the database with sample data
docker exec environmental-monitoring-system-backend-1 python /app/seed.py

# Stop services
docker compose down
```

**Access:**

- **Dashboard**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

## API Endpoints

| Method | Endpoint                   | Description                     |
| ------ | -------------------------- | ------------------------------- |
| `POST` | `/measurements`            | Create a new measurement        |
| `GET`  | `/measurements`            | List measurements with filters  |
| `GET`  | `/measurements/stats`      | Get aggregated statistics       |
| `GET`  | `/measurements/timeseries` | Get time-series data for charts |
| `GET`  | `/health`                 | Health check                    |

### Example Requests

**Create Measurement:**

```bash
curl -X POST https://alert-forgiveness-production.up.railway.app/measurements \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2026-04-02T10:30:00Z",
    "temperature": 23.5,
    "humidity": 65.0,
    "device_id": "sensor-01"
  }'
```

**Get Statistics:**

```bash
curl "https://alert-forgiveness-production.up.railway.app/measurements/stats"
```

**Get Time-Series Data:**

```bash
curl "https://alert-forgiveness-production.up.railway.app/measurements/timeseries?interval=day"
```

## Configuration

### Environment Variables

#### Backend

| Variable      | Description                           | Default                              |
| ------------- | ------------------------------------- | ------------------------------------ |
| `DATABASE_URL`| PostgreSQL connection string          | `sqlite+aiosqlite:///./env_monitoring.db` |
| `ENVIRONMENT` | `development` or `production`        | `development`                        |

#### Frontend

| Variable             | Description                    | Default                              |
| -------------------- | ------------------------------ | ------------------------------------ |
| `VITE_API_BASE_URL` | Backend API URL               | Railway production URL               |

### Railway Deployment

The backend is deployed on Railway with PostgreSQL:

1. Create project on Railway
2. Add PostgreSQL service
3. Deploy from GitHub (root: `backend`)
4. Railway automatically sets `DATABASE_URL`

### Vercel Deployment

The frontend is deployed on Vercel:

1. Import project from GitHub
2. Set root directory: `frontend`
3. Add environment variable:
   - `VITE_API_BASE_URL` = `https://alert-forgiveness-production.up.railway.app`
4. Deploy

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
- CORS configured for production

## License

MIT License

## Author

Ruben Quintana

## Acknowledgments

- FastAPI for the excellent async API framework
- PostgreSQL for reliable data storage
- Recharts for beautiful React charts
- Vite for lightning-fast development experience
