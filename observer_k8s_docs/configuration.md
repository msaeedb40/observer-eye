# Configuration & Secrets Management

The platform configuration is decoupled from the application logic via Kubernetes primitives.

## Environment Variables (ConfigMap)

The `observer-config` ConfigMap contains non-sensitive parameters:
- `DB_HOST`: Points to `db-service`.
- `REDIS_URL`: Points to `redis-service`.
- `BACKEND_URL`: Internal service URL for middleware-to-backend communication.
- `KAFKA_BROKERS`: Message broker endpoints.

## Sensitive Data (Secrets)

The `observer-secrets` Secret handles:
- `DB_PASSWORD`: Database credentials.
- `DJANGO_SECRET_KEY`: Cryptographic signing key.

> [!WARNING]
> In production environments, it is highly recommended to use a secret management solution like **HashiCorp Vault** or **AWS Secrets Manager** integrated with Kubernetes.

## Service Discovery
All components use Kubernetes DNS names (e.g., `db-service.observer-eye.svc.cluster.local`) for discovery, ensuring high portability across clusters.
