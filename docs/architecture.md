# Observer-Eye Architecture

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                              INTERNET                                 │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (Port 80)                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                     Angular 21 Frontend                          │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │
│  │  │Dashboard│ │ Metrics │ │  Logs   │ │ Traces  │ │ Alerts  │   │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │ HTTP/WebSocket
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      LOGIC LAYER (Port 8400)                          │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   FastAPI Middleware                             │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │ │
│  │  │Performance│ │ Caching   │ │ Streaming │ │ Telemetry │       │ │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐                     │ │
│  │  │Data Proc. │ │Error Hand.│ │ Testing   │                     │ │
│  │  └───────────┘ └───────────┘ └───────────┘                     │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                  │                                    │
│                           ┌──────┴──────┐                            │
│                           │    Redis    │                            │
│                           │   (Cache)   │                            │
│                           └─────────────┘                            │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │ HTTP/REST
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       DATA LAYER (Port 8000)                          │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    Django Backend                                │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │                    Observer Apps (19)                     │   │ │
│  │  │  Metrics: appmetrics, netmetrics, systemmetrics, security │   │ │
│  │  │  Performance: APM, identity, security, system, traffic    │   │ │
│  │  │  Analytics: analytics, insights_observer                  │   │ │
│  │  │  Platform: integration, notification, queriers, settings  │   │ │
│  │  └──────────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                  │                                    │
│                           ┌──────┴──────┐                            │
│                           │ PostgreSQL  │                            │
│                           │  (Database) │                            │
│                           └─────────────┘                            │
└──────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Angular 21 | User interface |
| Middleware | FastAPI | API gateway, data processing |
| Backend | Django + DRF | Business logic, data persistence |
| Database | PostgreSQL 16 | Data storage |
| Cache | Redis 7 | Performance optimization |
| Container | Docker | Deployment |

## Data Flow

1. User requests reach the Angular frontend
2. Frontend communicates with FastAPI middleware via HTTP/WebSocket
3. Middleware processes, caches, and forwards requests to Django backend
4. Backend persists data in PostgreSQL and returns responses
