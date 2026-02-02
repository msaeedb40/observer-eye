# Observer-Eye Platform Description

## Platform Description

Observer-Eye is a full-stack observability solution that integrates **metrics collection**, **log aggregation**, **distributed tracing**, and **event tracking** into a unified platform. It provides end-to-end visibility across your entire application ecosystem.

## Components

### Frontend (Presentation Layer)
- Built with **Angular 21**
- Modern, responsive UI with real-time updates
- OAuth authentication (GitHub, GitLab, Google, Microsoft)
- Interactive dashboards with customizable widgets

### Middleware (Logic Layer)
- Built with **FastAPI**
- High-performance data processing
- Real-time WebSocket streaming
- Intelligent caching layer
- Data transformation and validation

### Backend (Data Layer)
- Built with **Django** and **Django REST Framework**
- 19 specialized observer apps:
  - Metrics: appmetrics, netmetrics, systemmetrics, securitymetrics
  - Performance: APM, identity, security, system, traffic monitoring
  - Analytics: analytics, insights_observer
  - Platform: integration, notification, queriers, settings, template_dashboards

## Data Flow

```
User -> Frontend (Port 80) -> Middleware (Port 8400) -> Backend (Port 8000) -> PostgreSQL
```

## Security

- JWT-based authentication
- OAuth 2.0 support
- Role-based access control
- Encrypted data in transit and at rest
- Non-root Docker containers
