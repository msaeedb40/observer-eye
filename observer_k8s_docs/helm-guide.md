# Observer-Eye Helm Deployment Guide

The platform is packaged as a standard Helm chart for streamlined deployment and management.

## Prerequisites

- Helm v3+
- Kubernetes cluster with Istio installed
- Gateway API CRDs installed

## Configuration

The `values.yaml` file controls all deployment aspects:
- `images`: Image repository and tags.
- `scaling`: Replica counts and DaemonSet toggles.
- `istio`: Mesh security settings.
- `gateway`: Traffic routing configuration.

## Deployment Steps

1. **Dry Run**: Validate manifests without applying.
   ```bash
   helm install observer-eye ./observer_k8s/platform-chart --dry-run --debug
   ```

2. **Install**:
   ```bash
   helm install observer-eye ./observer_k8s/platform-chart --namespace observer-eye --create-namespace
   ```

3. **Upgrade**:
   ```bash
   helm upgrade observer-eye ./observer_k8s/platform-chart
   ```

## Customizing Values

You can override any value at runtime:
```bash
helm install observer-eye ./observer_k8s/platform-chart \
  --set scaling.backend.replicas=5 \
  --set config.debug="true"
```
