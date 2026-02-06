from django.db import models
from core.models import BaseModel

class TrafficStats(BaseModel):
    """Aggregated traffic statistics."""
    timestamp = models.DateTimeField(db_index=True)
    ingress_bytes = models.BigIntegerField(default=0)
    egress_bytes = models.BigIntegerField(default=0)
    total_requests = models.IntegerField(default=0)
    
    region = models.CharField(max_length=50, default='global')

    class Meta:
        verbose_name = 'Traffic Stats'
        verbose_name_plural = 'Traffic Stats'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.total_requests} reqs"

class RouteAnalytics(BaseModel):
    """Performance metrics per API route."""
    route_path = models.CharField(max_length=255)
    method = models.CharField(max_length=10) # GET, POST
    
    avg_latency_ms = models.FloatField(default=0.0)
    p95_latency_ms = models.FloatField(default=0.0)
    p99_latency_ms = models.FloatField(default=0.0)
    
    error_count = models.IntegerField(default=0)
    call_count = models.IntegerField(default=0)
    
    service = models.CharField(max_length=100) # Related service name

    class Meta:
        verbose_name = 'Route Analytics'
        verbose_name_plural = 'Route Analytics'
        unique_together = ['route_path', 'method', 'service']

    def __str__(self):
        return f"{self.method} {self.route_path}"

class LoadBalancerStats(BaseModel):
    """Load Balancer performance metrics."""
    lb_name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=50) # haproxy, nginx, alb
    
    active_connections = models.IntegerField(default=0)
    requests_per_second = models.FloatField(default=0.0)
    
    bytes_in = models.BigIntegerField(default=0)
    bytes_out = models.BigIntegerField(default=0)
    
    p99_latency_ms = models.FloatField(default=0.0)
    status_code_5xx = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Load Balancer Stats'
        verbose_name_plural = 'Load Balancer Stats'

    def __str__(self):
        return f"{self.lb_name} ({self.type})"
