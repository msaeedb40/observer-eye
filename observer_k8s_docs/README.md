# Observer-Eye Kubernetes Deployment

This directory contains the Kubernetes manifests for deploying the Observer-Eye platform at scale.

## Architecture

The K8s deployment follows a high-availability, 3-layer architecture enhanced with **Istio Service Mesh** and **Kubernetes Gateway API**.

### Infrastructure Layers
- **Namespace**: `observer-eye` (with Istio sidecar injection).
- **Service Mesh**: Istio (STRICT mTLS).
- **Ingress/Edge**: Kubernetes Gateway API (using Istio `gatewayClassName`).
- **Data Store**: PostgreSQL 16 (Stateful-style deployment with PVC).
- **Caching**: Redis 7 (with PVC).
- **Message Broker**: Kafka & Zookeeper for high-throughput telemetry.

### Application Layers
- **Backend (Django)**: 28 modular apps handling core platform logic.
- **Middleware (FastAPI)**: High-speed telemetry routing and AI enrichment.
- **Frontend (Angular)**: Signals-based Bento UI.
- **Async Workers**: Scalable Celery workers for predictive analytics.
- **Kafka Consumers**: Bridge between telemetry streams and processing tasks.

## Deployment Guide

1. **Install Gateway API CRDs** (if not present):
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
   ```

2. **Install Istio** (if not present):
   ```bash
   istioctl install --set profile=demo -y
   ```

3. **Apply Manifests**:
   ```bash
   kubectl apply -f observer_k8s/00-namespace.yaml
   kubectl apply -f observer_k8s/
   ```

## Traffic Management

External traffic is managed via the `observer-gateway` (Gateway) and `observer-frontend-route` (HTTPRoute). Internal traffic between services is protected by Istio's mTLS and can be monitored via Kiali.
