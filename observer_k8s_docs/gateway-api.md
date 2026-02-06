# Gateway API & Istio Traffic Flow

Observer-Eye uses the **Kubernetes Gateway API** for North-South traffic and **Istio** for East-West security.

## North-South Traffic (External to Mesh)

1. **Gateway**: `observer-gateway` listens on port 80.
2. **HTTPRoute**: `observer-frontend-route` matches `/` and forwards to the `frontend` service.
3. **Ingress Gateway**: Istio's ingress gateway handles the actual traffic termination and routing to pods.

## East-West Traffic (Service-to-Service)

1. **mTLS**: Enforced across the `observer-eye` namespace via `PeerAuthentication`.
2. **Reactivity**: Frontend communicates with `middleware-service` via standard K8s DNS.
3. **DaemonSet Middleware**: Since middleware is a `DaemonSet`, traffic can be optimized for node-local processing if desired using `InternalTrafficPolicy: Local` (optional).

## Monitoring Flow

All traffic passing through the mesh is automatically captured by Istio, allowing for:
- Transparent tracing.
- Golden metrics (Request rate, Error rate, Latency).
- Visual topology mapping in Kiali.
