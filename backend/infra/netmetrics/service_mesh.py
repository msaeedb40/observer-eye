"""
Service Mesh and Advanced Network models for Observer-Eye Platform.
Tracks service mesh (Istio/Linkerd), DNS, and TLS certificate metrics.
"""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class ServiceMeshMetric(BaseModel, ObservabilityMixin):
    """Service mesh (Istio/Linkerd) traffic metrics."""
    source_service = models.CharField(max_length=255, db_index=True)
    source_namespace = models.CharField(max_length=255, db_index=True)
    source_version = models.CharField(max_length=100, blank=True)
    
    destination_service = models.CharField(max_length=255, db_index=True)
    destination_namespace = models.CharField(max_length=255, db_index=True)
    destination_version = models.CharField(max_length=100, blank=True)
    
    # Traffic
    request_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    
    # Latency percentiles
    latency_p50_ms = models.FloatField(default=0.0)
    latency_p90_ms = models.FloatField(default=0.0)
    latency_p95_ms = models.FloatField(default=0.0)
    latency_p99_ms = models.FloatField(default=0.0)
    
    # Resilience
    retries = models.IntegerField(default=0)
    timeouts = models.IntegerField(default=0)
    circuit_breaker_open = models.BooleanField(default=False)
    connection_pool_exhausted = models.IntegerField(default=0)
    
    # Protocol
    protocol = models.CharField(max_length=20, default='http')  # http, grpc, tcp
    response_flags = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Service Mesh Metric'
        verbose_name_plural = 'Service Mesh Metrics'
        indexes = [
            models.Index(fields=['source_service', 'destination_service', 'timestamp']),
            models.Index(fields=['source_namespace', 'destination_namespace']),
        ]

    def __str__(self):
        return f"{self.source_service} -> {self.destination_service}"

    @property
    def success_rate(self):
        if self.request_count == 0:
            return 100.0
        return (self.success_count / self.request_count) * 100


class DNSMetric(BaseModel, ObservabilityMixin):
    """DNS resolution metrics."""
    host = models.CharField(max_length=255, db_index=True)
    query_domain = models.CharField(max_length=255, db_index=True)
    query_type = models.CharField(
        max_length=20,
        choices=[
            ('A', 'A'),
            ('AAAA', 'AAAA'),
            ('CNAME', 'CNAME'),
            ('MX', 'MX'),
            ('TXT', 'TXT'),
            ('NS', 'NS'),
            ('PTR', 'PTR'),
            ('SRV', 'SRV'),
        ],
        default='A'
    )
    
    response_time_ms = models.FloatField()
    resolver = models.CharField(max_length=255)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('nxdomain', 'NXDOMAIN'),
            ('servfail', 'SERVFAIL'),
            ('timeout', 'Timeout'),
            ('refused', 'Refused'),
        ],
        default='success'
    )
    
    # Response details
    response_ip = models.GenericIPAddressField(null=True, blank=True)
    ttl_seconds = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'DNS Metric'
        verbose_name_plural = 'DNS Metrics'

    def __str__(self):
        return f"{self.query_domain} ({self.query_type}): {self.status}"


class TLSCertificate(BaseModel):
    """TLS certificate monitoring."""
    host = models.CharField(max_length=255, db_index=True)
    port = models.IntegerField(default=443)
    domain = models.CharField(max_length=255, db_index=True)
    
    # Certificate details
    issuer = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100)
    
    # Validity
    not_before = models.DateTimeField()
    not_after = models.DateTimeField()
    days_until_expiry = models.IntegerField()
    
    # Security
    fingerprint_sha256 = models.CharField(max_length=64)
    signature_algorithm = models.CharField(max_length=50)
    key_size = models.IntegerField()
    
    # Status
    is_valid = models.BooleanField(default=True)
    validation_errors = models.JSONField(default=list, blank=True)
    
    # Chain
    chain_length = models.IntegerField(default=0)
    chain_valid = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'TLS Certificate'
        verbose_name_plural = 'TLS Certificates'
        unique_together = ['host', 'port', 'domain']

    def __str__(self):
        return f"{self.domain} (expires in {self.days_until_expiry} days)"


class ServiceDependency(BaseModel):
    """Service dependency mapping for topology."""
    source_service = models.CharField(max_length=255, db_index=True)
    source_namespace = models.CharField(max_length=255, blank=True)
    
    target_service = models.CharField(max_length=255, db_index=True)
    target_namespace = models.CharField(max_length=255, blank=True)
    
    dependency_type = models.CharField(
        max_length=50,
        choices=[
            ('http', 'HTTP'),
            ('grpc', 'gRPC'),
            ('tcp', 'TCP'),
            ('database', 'Database'),
            ('cache', 'Cache'),
            ('queue', 'Message Queue'),
        ],
        default='http'
    )
    
    # Discovery
    discovered_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Health
    avg_latency_ms = models.FloatField(default=0.0)
    error_rate = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Service Dependency'
        verbose_name_plural = 'Service Dependencies'
        unique_together = ['source_service', 'target_service', 'dependency_type']

    def __str__(self):
        return f"{self.source_service} -> {self.target_service} ({self.dependency_type})"
