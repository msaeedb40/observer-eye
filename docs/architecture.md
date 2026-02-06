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
│  │         Angular 21 (Signals + Bento Grid)              │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │ │
│  │  │ Dashboard│ │ Performance│ │  Alerts  │ │ Analytics│ │ Settings │ │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │ HTTP/WebSocket
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      LOGIC LAYER (Port 8400)                          │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   FastAPI Middleware                             │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │ │
│  │  │   Router  │ │ Enrichment│ │ Streaming │ │ Anomaly   │       │ │
│  │  └─────┬─────┘ └─────┬─────┘ └───────────┘ └───────────┘       │ │
│  └────────│─────────────│──────────────────────────────────────────┘ │
│           ▼             ▼                                            │
│  ┌───────────────────────────────┐      ┌─────────────────────────┐  │
│  │      Kafka Message Bus        │ ──▶  │     Celery Workers      │  │
│  │  (High-Throughput Ingestion)  │      │  (Async Processing)     │  │
│  └───────────────────────────────┘      └────────────┬────────────┘  │
│                                                      │               │
│                                               ┌──────▼──────┐        │
│                                               │    Redis    │        │
│                                               │  (Broker)   │        │
│                                               └─────────────┘        │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │ HTTP/REST
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       DATA LAYER (Port 8000)                          │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    Django Backend                                │ │
│  │  ┌──────────────────────────────────────────────────────────┐   │ │
│  │  │                    Observer Apps (28)                     │   │ │
│  │  │  Observability: appmetrics, netmetrics, systemmetrics      │   │ │
│  │  │  Infrastructure: cloud, kubernetes, containers             │   │ │
│  │  │  Security: securitymetrics, compliance, incidents          │   │ │
│  │  │  Analytics: analytics, insights_observer, ai_engine        │   │ │
│  │  │  Platform: integration, notification, settings             │   │ │
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
| Frontend | Angular 21 + Signals | Bento UI, Fine-grained reactivity, OnPush |
| Mesh | Istio 1.22+ | mTLS, Sidecar injection, Zero-trust security |
| Ingress | Gateway API | Traffic orchestration, TLS termination |
| Identity | OIDC / JWT | Social Auth (Google, GitHub, GitLab), RBAC |
| Middleware | FastAPI | DaemonSet-based enrichment, API Gateway |
| Message Bus | Kafka | Real-time telemetry ingestion |
| Task Queue | Celery | Predictive analytics, Async processing |
| Backend | Django 5.x | Platform logic, Policy engine |
| Database | PostgreSQL 16 | Relational persistence |
| Cache | Redis 7 | Real-time caching & Celery broker |
| Runtime | K8s + Docker | Production-grade orchestration |

## Data Flow

1. User requests reach the Angular frontend
2. Frontend communicates with FastAPI middleware via HTTP/WebSocket
3. Middleware processes, caches, and forwards requests to Django backend
4. Backend persists data in PostgreSQL and returns responses
