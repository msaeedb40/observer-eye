# Observer-Eye Observability Platform

## Overview

Observer-Eye is a comprehensive observability platform built on a **3-layer architecture** and implementing the **4 pillars of observability**: Metrics, Events, Logs, and Traces.

## Key Features

- **Real-time Monitoring** - Track system health and performance in real-time
- **Distributed Tracing** - End-to-end request tracing across services
- **Log Aggregation** - Centralized log collection and search
- **Metric Visualization** - Beautiful dashboards for metrics analysis
- **Alert Management** - Configurable alerts with multiple notification channels
- **Performance Monitoring** - APM for applications, systems, network, and security

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet / Users                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              Presentation Layer (Angular 21)                 │
│                       Port 80                                │
│  • Dashboard  • Metrics  • Logs  • Traces  • Alerts         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              Logic Layer (FastAPI Middleware)                │
│                      Port 8400                               │
│  • Data Processing  • Caching  • Streaming  • Telemetry     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│               Data Layer (Django Backend)                    │
│                      Port 8000                               │
│  • 19 Observer Apps  • REST APIs  • PostgreSQL              │
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