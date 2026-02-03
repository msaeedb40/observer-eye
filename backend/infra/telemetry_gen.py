import os
import time
import random
import django
import uuid
from datetime import datetime, timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infra.settings')
django.setup()

from core.models import Metric, Event, LogEntry, Trace, Span
from appmetrics.models import ApplicationMetric, EndpointMetric
from netmetrics.models import NetworkMetric, ConnectionMetric
from systemmetrics.models import SystemMetric, DiskMetric, ProcessMetric
from securitymetrics.models import SecurityMetric, ThreatEvent, AuditLog
from application_performance_monitoring.models import APMTransaction, APMSpan, APMError
from grailobserver.models import GrailEntity, GrailRelationship

def generate_core_metrics():
    """Generate basic core metrics."""
    sources = ['api-gateway', 'auth-service', 'worker-1', 'db-01']
    metrics = ['cpu_usage', 'memory_usage', 'disk_io', 'network_latency', 'active_users']
    
    for metric_name in metrics:
        source = random.choice(sources)
        Metric.objects.create(
            name=metric_name,
            value=random.uniform(10, 95) if 'usage' in metric_name else random.uniform(1, 100),
            unit='%' if 'usage' in metric_name else 'ms' if 'latency' in metric_name else 'units',
            source=source,
            metric_type='gauge'
        )

def generate_app_metrics():
    """Generate app-specific performance metrics."""
    apps = ['frontend', 'middleware', 'backend', 'auth-service']
    environments = ['production', 'staging']
    
    for app in apps:
        ApplicationMetric.objects.create(
            app_name=app,
            environment=random.choice(environments),
            source=f"{app}-v1",
            request_count=random.randint(100, 5000),
            error_count=random.randint(0, 50),
            avg_latency_ms=random.uniform(20, 150),
            requests_per_second=random.uniform(5, 50)
        )
        
        EndpointMetric.objects.create(
            app_name=app,
            endpoint=f"/api/v1/{random.choice(['users', 'data', 'auth', 'health'])}",
            method=random.choice(['GET', 'POST']),
            request_count=random.randint(50, 1000),
            error_count=random.randint(0, 10),
            avg_latency_ms=random.uniform(10, 100),
            source=f"{app}-v1"
        )

def generate_net_metrics():
    """Generate network and connection metrics."""
    hosts = ['node-01', 'node-02', 'db-cluster-01', 'proxy-01']
    
    for host in hosts:
        NetworkMetric.objects.create(
            host=host,
            interface='eth0',
            source='node-exporter',
            bytes_sent=random.randint(10**6, 10**9),
            bytes_received=random.randint(10**6, 10**9),
            latency_ms=random.uniform(0.1, 5.0)
        )
        ConnectionMetric.objects.create(
            host=host,
            source='netstat',
            active_connections=random.randint(10, 1000),
            established_connections=random.randint(5, 800)
        )

def generate_system_metrics():
    """Generate detailed system metrics."""
    hosts = ['server-prod-01', 'server-prod-02', 'server-prod-03']
    
    for host in hosts:
        SystemMetric.objects.create(
            host=host,
            hostname=f"{host}.local",
            source='system-agent',
            cpu_percent=random.uniform(5, 80),
            memory_percent=random.uniform(20, 90),
            memory_total_bytes=16 * 1024**3,
            load_avg_1min=random.uniform(0.1, 4.0)
        )
        DiskMetric.objects.create(
            host=host,
            mount_point='/',
            device='/dev/sda1',
            source='disk-monitor',
            usage_percent=random.uniform(30, 85)
        )

def generate_security_metrics():
    """Generate security alerts and metrics."""
    hosts = ['bastion-01', 'api-gateway']
    
    for host in hosts:
        SecurityMetric.objects.create(
            host=host,
            source='fail2ban',
            auth_attempts=random.randint(100, 500),
            auth_failures=random.randint(0, 20),
            blocked_requests=random.randint(0, 50)
        )
        if random.random() < 0.1:
            ThreatEvent.objects.create(
                host=host,
                source='ids-snort',
                threat_type=random.choice(['SQL Injection', 'Brute Force', 'DDoS Pattern']),
                severity=random.choice(['medium', 'high', 'critical']),
                description="Detected suspicious payload in HTTP header",
                source_ip=f"192.168.1.{random.randint(1, 254)}",
                blocked=True
            )

def generate_apm_data():
    """Generate APM transactions and errors."""
    apps = ['payment-service', 'inventory-api', 'user-profile']
    
    for app in apps:
        if random.random() < 0.4:
            tx = APMTransaction.objects.create(
                app_name=app,
                source='apm-agent',
                transaction_name=random.choice(['CheckInventory', 'ProcessPayment', 'GetUserProfile']),
                duration_ms=random.uniform(50, 500),
                result='error' if random.random() < 0.05 else 'success',
                http_method='POST',
                http_status_code=500 if random.random() < 0.05 else 200
            )
            
            # Simple span for the transaction
            APMSpan.objects.create(
                transaction=tx,
                name='DatabaseQuery',
                span_type='db',
                duration_ms=tx.duration_ms * 0.7
            )
            
            if tx.result == 'error':
                APMError.objects.create(
                    app_name=app,
                    source='apm-agent',
                    error_type='ConnectionPoolTimeout',
                    message="Timeout waiting for database connection",
                    transaction_name=tx.transaction_name,
                    trace_id=tx.trace_id
                )

def generate_events():
    """Generate synthetic core events."""
    event_types = ['deploy', 'health_check', 'auth_failure', 'scaling']
    sources = ['kubernetes-master', 'github-actions', 'auth-service']
    severities = ['info', 'warning', 'error', 'critical']
    
    if random.random() < 0.3:
        Event.objects.create(
            name=f"Event_{uuid.uuid4().hex[:8]}",
            event_type=random.choice(event_types),
            severity=random.choice(severities),
            source=random.choice(sources),
            data={'msg': 'Synthetic event generated', 'code': random.randint(100, 500)}
        )

def generate_logs():
    """Generate synthetic logs."""
    levels = ['debug', 'info', 'warning', 'error', 'critical']
    sources = ['backend-app', 'middleware-api', 'auth-worker']
    
    for _ in range(random.randint(1, 5)):
        LogEntry.objects.create(
            level=random.choice(levels),
            message=f"Synthetic log message {uuid.uuid4().hex[:12]}",
            source=random.choice(sources),
            trace_id=str(uuid.uuid4())
        )

def generate_traces():
    """Generate synthetic traces and spans."""
    services = ['gateway', 'auth', 'billing', 'inventory']
    
    if random.random() < 0.2:
        trace_id = str(uuid.uuid4())
        main_trace = Trace.objects.create(
            name=f"Request_{services[0]}",
            trace_id=trace_id,
            service_name=services[0],
            start_time=datetime.now(timezone.utc),
            duration_ms=random.randint(100, 1000),
            status='ok' if random.random() > 0.1 else 'error'
        )
        
        for i, service in enumerate(services[1:], 1):
            Span.objects.create(
                trace=main_trace,
                span_id=str(uuid.uuid4())[:16],
                name=f"Call_{service}",
                start_time=datetime.now(timezone.utc),
                duration_ms=random.randint(20, 200),
                status='ok'
            )

def generate_grail_graph():
    """Generate or update Grail topological graph."""
    # Define entities
    entities = [
        {"id": "fe-01", "name": "Frontend Cluster", "type": "service_group"},
        {"id": "api-gw", "name": "API Gateway", "type": "service"},
        {"id": "auth-srv", "name": "Auth Service", "type": "service"},
        {"id": "pay-srv", "name": "Payment Service", "type": "service"},
        {"id": "inv-srv", "name": "Inventory Service", "type": "service"},
        {"id": "pg-cluster", "name": "Postgres Main", "type": "database"},
        {"id": "redis-01", "name": "Redis Cache", "type": "cache"},
        {"id": "k8s-node-1", "name": "Kubernetes Node 1", "type": "host"},
        {"id": "k8s-node-2", "name": "Kubernetes Node 2", "type": "host"},
    ]
    
    entity_objs = {}
    for e in entities:
        obj, _ = GrailEntity.objects.update_or_create(
            entity_id=e["id"],
            defaults={
                "display_name": e["name"],
                "entity_type": e["type"],
                "health_status": random.choice(['healthy', 'healthy', 'healthy', 'degraded']),
                "last_seen": datetime.now(timezone.utc),
                "properties": {"version": "v1.2.4", "region": "us-east-1"}
            }
        )
        entity_objs[e["id"]] = obj
        
    # Define relationships
    relationships = [
        ("fe-01", "api-gw", "calls"),
        ("api-gw", "auth-srv", "calls"),
        ("api-gw", "pay-srv", "calls"),
        ("api-gw", "inv-srv", "calls"),
        ("pay-srv", "pg-cluster", "queries"),
        ("inv-srv", "pg-cluster", "queries"),
        ("auth-srv", "redis-01", "uses"),
        ("api-gw", "k8s-node-1", "runs_on"),
        ("pay-srv", "k8s-node-2", "runs_on"),
    ]
    
    for src_id, tgt_id, rel_type in relationships:
        if src_id in entity_objs and tgt_id in entity_objs:
            GrailRelationship.objects.update_or_create(
                source=entity_objs[src_id],
                target=entity_objs[tgt_id],
                relationship_type=rel_type
            )

def main():
    """Main loop for telemetry generation."""
    print("🚀 Telemetry generator started...")
    while True:
        try:
            generate_core_metrics()
            generate_app_metrics()
            generate_net_metrics()
            generate_system_metrics()
            generate_security_metrics()
            generate_apm_data()
            generate_events()
            generate_logs()
            generate_traces()
            generate_grail_graph()
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Telemetry data generated.")
            time.sleep(5)  # Generate data every 5 seconds
        except Exception as e:
            print(f"❌ Error generating data: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
