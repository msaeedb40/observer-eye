# Scaling & Resource Management

Observer-Eye is designed to scale horizontally across all layers.

## Component Scaling Strategies

| Component | Scaling Type | Strategy |
|-----------|--------------|----------|
| **Frontend** | Horizontal | Scaled via `replicas` in Deployment. |
| **Middleware** | Node-Local | Runs as a `DaemonSet`, automatically scaling with cluster nodes. |
| **Backend** | Horizontal | Scaled via HPA based on CPU/Memory utilization. |
| **Workers** | Task-Based | Scaled based on Celery queue depth/latency. |
| **Postgres** | Vertical | Currently a single instance with PVC. Use StateFulSet for HA if required. |

## Horizontal Pod Autoscaling (HPA)

To enable HPA for the backend, apply the Following policy:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: observer-eye
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Resource Requests & Limits
Each deployment contains resource definitions to ensure fair scheduling and stability. See individual manifest files for details.
