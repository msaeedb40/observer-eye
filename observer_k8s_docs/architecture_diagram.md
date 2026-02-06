# Observer-Eye Platform Architecture

This diagram illustrates the high-level architecture of the Observer-Eye platform, highlighting the Kubernetes orchestration, Istio service mesh, Identity & SSO stack, and the 4-pillar observability data flow.

```mermaid
graph TD
    subgraph "External Ecosystem"
        User["🌐 User / Client Browser"]
        OIDC["🔐 OIDC Providers (Google, GitHub, GitLab)"]
    end

    subgraph "Kubernetes Cluster (observer-eye namespace)"
        Gateway["🌉 Kubernetes Gateway (Istio Ingress)"]
        
        subgraph "Istio Service Mesh (mTLS Enabled)"
            subgraph "Presentation Layer"
                Frontend["🎬 Angular Web App (OnPush/Signals)"]
            end
            
            subgraph "Middleware Layer (DaemonSet)"
                Middleware["⚙️ FastAPI Middleware Proxy"]
                IdentityProxy["🆔 OAuth & Domain Restriction Handler"]
                TelemetryIngest["📊 Telemetry Ingestion Engine"]
                DataProcessor["🧠 Data Processing Service"]
            end
            
            subgraph "Backend Layer (Django)"
                Backend["🔌 Django Backend API"]
                IdentitySvc["🔐 Identity Svc (JWT/Social Auth)"]
                MetricSvc["📈 Metrics Service"]
                TraceSvc["⛓️ Tracing Service"]
                LogSvc["📄 Logs Service"]
            end
        end

        subgraph "Infrastructure Layer"
            Kafka["🚀 Kafka Message Bus (Zookeeper)"]
            Redis["⚡ Redis Cache / Pub-Sub"]
            Postgres["💾 PostgreSQL Database"]
        end
    end

    %% Authentication Flow
    User -->|Access (HTTPS)| Gateway
    Gateway --> Frontend
    Frontend -->|Social Login Request| OIDC
    OIDC -->|Verification Callback| Gateway
    Gateway --> IdentityProxy
    IdentityProxy -->|Domain Restriction Check| IdentityProxy
    IdentityProxy -->|Verify & Exchange Token| IdentitySvc
    IdentitySvc -->|Issue Platform JWT| IdentityProxy
    IdentityProxy -->|Identity Handshake| User

    %% Data Flow (4 Pillars of Observability)
    Middleware -->|Capture: Metrics, Logs, Traces| TelemetryIngest
    TelemetryIngest -->|Asynchronous Stream| Kafka
    Kafka -->|Batch Processing| DataProcessor
    DataProcessor -->|Real-time Cache| Redis
    DataProcessor -->|Long-term Storage| Postgres
    
    %% API Operations
    Frontend -->|Secured API Calls (JWT)| Gateway
    Gateway --> Middleware
    Middleware -->|Identity/Performance Proxy| Backend
    Backend -->|Query History/Metadata| Postgres
    Backend -->|Fast Lookup / State| Redis

    %% Styling
    classDef primary fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef secondary fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
    classDef infra fill:#f5f5f5,stroke:#9e9e9e,stroke-width:1px;
    classDef highlight fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;

    class Gateway,Frontend,Middleware,Backend primary;
    class IdentityProxy,IdentitySvc,TelemetryIngest,DataProcessor secondary;
    class Kafka,Redis,Postgres infra;
    class OIDC,User highlight;
```

## Key Architectural Components

### 1. Traffic Management (Ingress)
All incoming traffic is managed by the **Kubernetes Gateway API** and the **Istio Ingress Gateway**. This ensures a single point of entry for security, rate limiting, and mTLS termination.

### 2. Identity & Security
- **OAuth 2.0 / OIDC**: Native integration with social providers.
- **Middleware Proxy**: Handles the initial OIDC handshake and enforces **Organization Domain Restrictions**.
- **JWT**: The backend issues short-lived JWTs for secured API access.
- **mTLS**: Istio enforces `STRICT` mutual TLS for all inter-pod communications.

### 3. Observability Pipeline
- **DaemonSet Middleware**: Ensures telemetry capture at the node level.
- **Kafka-Driven**: High-throughput message bus for decoupling ingestion from processing.
- **4 Pillars**: Unified processing of Metrics, Events, Logs, and Traces (MELT).

### 4. Presentation Layer
- **Angular 19**: Built with **Signals** and `OnPush` change detection for maximum UI performance and reactivity.
