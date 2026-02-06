# Observer-Eye User Guide

## Quick Start

### 🐳 Option 1: Docker Compose (Development)
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd observer-eye
   ```
2. Start the services:
   ```bash
   docker-compose up -d
   ```
3. Access: `http://localhost:80`

### ☸️ Option 2: Kubernetes (Production)
1. **Helm Deployment**:
   ```bash
   cd observer_k8s/platform-chart
   helm install observer-eye-platform . -n observer-eye --create-namespace
   ```
2. **Access**:
   ```bash
   kubectl port-forward svc/observer-frontend 8080:80 -n observer-eye
   ```
   Open `http://localhost:8080`

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
- **Real-time Dashboard** - Live monitoring with auto-refresh
- **Application Performance Monitoring (APM)** - Response times, throughput, error rates
- **Cloud & Kubernetes Monitoring** - AWS/Azure/GCP cost and health; Pod/Deployment tracking
- **Infrastructure Monitoring** - System, network, and security metrics
- **AI-Powered Insights** - Automated anomaly detection and predictive forecasting
- **Alert Management** - Configurable thresholds with multi-channel notifications
- **Analytics & Settings** - BI-powered analysis and comprehensive workspace configuration
  - **Incidents**: Centralized incident response
- **Metrics/Logs/Traces** - Traditional observability explorers
- **Settings** - Comprehensive workspace management:
  - **General**: System-wide preferences
  - **Alerts**: Notification channels and alert rules
  - **Integrations**: AWS, Slack, PagerDuty, etc.
  - **AI/ML**: Engine sensitivity and forecasting
  - **Security**: API keys and SSO
  - **Billing**: Usage-based cost management

## Platform CLI

The `observercli.py` script provides a unified interface for managing the platform:

```bash
# Check platform health
./observercli.py health

# Start/Stop platform
./observercli.py start
./observercli.py stop

# View status of all services
./observercli.py status

# Purge all data (USE WITH CAUTION)
./observercli.py purge
```

## Configuration

The platform is configured via environment variables, which can be managed via `docker-compose.yml` or Kubernetes **ConfigMaps**.

| Key | Description | Default |
|-----|-------------|---------|
| `BACKEND_URL` | URL of the Django Backend | `http://backend:8000` |
| `MIDDLEWARE_PORT` | FastAPI Logic Layer port | `8400` |
| `DB_HOST` | PostgreSQL host | `postgres` |

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
