# Istio Service Mesh Configuration

## Security Model

The Observer-Eye mesh is secured by **STRICT mTLS**.

### PeerAuthentication
We use a global-to-namespace policy to ensure only encrypted traffic is allowed between services:

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: observer-eye
spec:
  mtls:
    mode: STRICT
```

## Security Policies

### RequestAuthentication
Enforces JWT validation for all requests entering the mesh. This is integrated with our OIDC flow:

```yaml
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: observer-eye
spec:
  jwtRules:
  - issuer: "observer-eye-backend"
    jwksUri: "http://backend.observer-eye.svc.cluster.local:8000/api/v1/auth/jwks/"
```

### AuthorizationPolicy
Enforces strict domain-based access and valid JWT requirements:

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-authenticated
  namespace: observer-eye
spec:
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]
    to:
    - operation:
        methods: ["GET", "POST"]
```

## Sidecar Injection
Automatic sidecar injection is enabled via the namespace label:
`istio-injection=enabled`

## Observability
With the sidecars in place, you can view real-time traffic flows:
- `istioctl dashboard kiali`: Topology map.
- `istioctl dashboard jaeger`: Trace analysis.
- `istioctl dashboard prometheus`: Service metrics.
