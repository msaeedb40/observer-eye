# Observer-Eye Platform Overview

## What is Observer-Eye?

Observer-Eye is a high-fidelity, cloud-native observability platform designed to provide total visibility into application infrastructures. Built on a container-first architecture and implementing zero-trust security principles, it delivers real-time insights across metrics, events, logs, and traces.

## Core Capabilities

### 4 Pillars of Observability

| Pillar | Description | Implementation |
|--------|-------------|----------------|
| **Metrics** | Numerical measurements over time | PromQL-compatible ingestion & querying |
| **Events** | Discrete occurrences with context | Event-driven alerting and AI correlation |
| **Logs** | Timestamped text records | High-speed structured log streaming |
| **Traces** | Request flow across services | Istio-sidecar distributed span collection |

### Key Features

- **Zero-Mock Policy** - 100% real-time data flow with no synthetic placeholders.
- **Premium Bento Grid Dashboard** - High-density, responsive monitoring using Angular 21 Signals.
- **Zero-Trust Infrastructure** - Enforced mTLS with Istio and OIDC identity validation.
- **Predictive Analytics** - 90% MTTR/MTTS compatibility using async AI-model workers.
- **DaemonSet Enrichment** - Low-latency telemetry processing scaling with your cluster.

## Architecture

Observer-Eye follows a strictly decoupled 3-layer architecture:

1. **Presentation Layer** - Angular 21 (Signals-based) frontend on port 80.
2. **Logic Layer** - FastAPI middleware + Istio Service Mesh on port 8400.
3. **Data Layer** - Django backend with 28 modular apps and PostgreSQL.

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
