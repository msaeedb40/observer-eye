# Network Security & Policies

Observer-Eye implements a **Zero-Trust Network Model** within Kubernetes using standard `NetworkPolicy` resources.

## Philosophy

By default, all ingress traffic to pods in the `observer-eye` namespace is denied. Traffic is only permitted between components that have a defined functional relationship.

## Policy breakdown

### 1. Default Deny
- **Manifest**: `templates/network-policies.yaml` (`deny-all`)
- **Action**: Drops all incoming traffic to any pod in the namespace unless explicitly allowed.

### 2. Frontend Access
- **Allowed From**: Istio Gateway.
- **Purpose**: Allows external users to reach the Angular dashboard.

### 3. Middleware Ingest
- **Allowed From**: `frontend` pods.
- **Purpose**: Permits API requests and telemetry ingestion from the presentation layer.

### 4. Backend Core
- **Allowed From**: `middleware` pods and `worker` pods.
- **Purpose**: Restricts database operations and policy checks to logical processing layers.

### 5. Infrastructure Access
- **DB/Redis/Kafka**: Only accessible from `backend`, `middleware`, or `worker` pods based on their specific role.

## Mesh Interaction

These policies work in tandem with **Istio mTLS**. While Istio ensures the traffic is encrypted and authenticated at the transport layer, NetworkPolicies enforce authorization at the IP/Pod layer, providing a defense-in-depth security posture.
