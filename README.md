# Observer-Eye Observability Platform

## Overview

Observer-Eye is a high-fidelity, cloud-native observability platform built on a **3-layer architecture** and implementing the **4 pillars of observability**: Metrics, Events, Logs, and Traces.

- **Cloud-Native Integration** - Optimized for 100% production-ready deployments on Kubernetes with Istio Service Mesh.
- **Premium Bento Grid Dashboard** - High-density, responsive 12-column grid layout with Angular 21 Signals.
- **Zero-Trust Security** - STRICT mTLS and OIDC-based Identity (Google, GitHub, GitLab) with organization domain enforcement.
- **Zero-Mock Policy** - Strictly real-time telemetry datasets with no synthetic or sample data.
- **Distributed Tracing** - End-to-end request tracing and span analysis.
- **AI-Powered Insights** - Anomaly detection, health scoring, and predictive forecasting.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet / Users                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              Presentation Layer (Angular 21)                 │
│                       Port 80                                │
│  • Signals Reactivity • Bento UI • OIDC Auth • OnPush        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│           Logic Layer (FastAPI / Istio Mesh)                 │
│                      Port 8400                               │
│  • DaemonSet Enrichment • mTLS • Gateway API • Telemetry    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│               Data Layer (Django Backend)                    │
│                      Port 8000                               │
│  • 28 Modular Apps • REST APIs • Zero-Mock Policy           │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd observer-eye

# Start with Docker Compose
docker-compose up -d

# Access the platform
open http://localhost:80
```

## Technology Stack

| Layer        | Technology     | Version |
|--------------|----------------|---------|
| Frontend     | Angular        | 21      |
| Middleware   | FastAPI        | 0.109+  |
| Backend      | Django         | 5.0+    |
| Database     | PostgreSQL     | 16      |
| Cache        | Redis          | 7       |

## 4 Pillars of Observability

1. **Metrics** - Quantitative measurements over time
2. **Events** - Discrete occurrences with context
3. **Logs** - Timestamped text records
4. **Traces** - Request flow across services

## License

MIT License