# Observer-Eye User Guide

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- 4GB RAM minimum
- Ports 80, 8000, 8400 available

### Starting the Platform

```bash
# Clone repository
git clone <repository-url>
cd observer-eye

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Accessing the Platform

- **Frontend**: http://localhost:80
- **Middleware API**: http://localhost:8400/docs
- **Backend Admin**: http://localhost:8000/admin

## Authentication

### Standard Login
1. Navigate to http://localhost/auth/login
2. Enter email and password
3. Password requirements: 16+ chars, mixed case, numbers, special chars

### OAuth Login
Click the OAuth provider button:
- GitHub
- GitLab
- Google
- Microsoft

## Using the Dashboard

### Navigation
- **Dashboard** - Overview with key metrics
- **Metrics** - Metric explorer
- **Events** - Event timeline
- **Logs** - Log viewer
- **Traces** - Distributed tracing
- **Alerts** - Alert management
- **Settings** - Configuration

## API Usage

### Health Check
```bash
curl http://localhost:8400/health
```

### Metrics
```bash
# Get metrics
curl http://localhost:8400/api/v1/telemetry/metrics

# Record metrics
curl -X POST http://localhost:8400/api/v1/telemetry/metrics \
  -H "Content-Type: application/json" \
  -d '[{"name": "cpu_usage", "value": 45.2}]'
```

## Stopping the Platform

```bash
docker-compose down

# To also remove volumes
docker-compose down -v
```
