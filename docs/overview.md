# Observer-Eye Platform Overview

## What is Observer-Eye?

Observer-Eye is an enterprise-grade observability platform designed to provide comprehensive visibility into your application infrastructure. Built on modern technologies and implementing industry best practices, it delivers real-time insights across all layers of your technology stack.

## Core Capabilities

### 4 Pillars of Observability

| Pillar | Description | Use Case |
|--------|-------------|----------|
| **Metrics** | Numerical measurements over time | CPU usage, request latency, error counts |
| **Events** | Discrete occurrences with context | Deployments, configuration changes, incidents |
| **Logs** | Timestamped text records | Application logs, access logs, error logs |
| **Traces** | Request flow across services | Distributed tracing, dependency mapping |

### Key Features

- **Real-time Dashboard** - Live monitoring with auto-refresh
- **Application Performance Monitoring (APM)** - Response times, throughput, error rates
- **Infrastructure Monitoring** - System, network, and security metrics
- **Alert Management** - Configurable thresholds with multi-channel notifications
- **Analytics & Insights** - BI-powered analysis and recommendations

## Architecture

Observer-Eye follows a 3-layer architecture:

1. **Presentation Layer** - Angular 21 frontend on port 80
2. **Logic Layer** - FastAPI middleware on port 8400
3. **Data Layer** - Django backend with PostgreSQL

## Getting Started

```bash
docker-compose up -d
open http://localhost:80
```

## Target Users

- **DevOps Engineers** - Infrastructure monitoring
- **SRE Teams** - Incident response and reliability
- **Development Teams** - Application debugging
- **Security Teams** - Security monitoring and compliance
