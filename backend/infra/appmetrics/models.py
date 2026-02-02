"""
Application Metrics models for Observer-Eye Platform.
Tracks application-level metrics: requests, latency, errors.
"""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class ApplicationMetric(BaseModel, ObservabilityMixin):
    """Application-level metric (request latency, error counts, etc.)."""
    app_name = models.CharField(max_length=255, db_index=True)
    environment = models.CharField(max_length=50, default='production', db_index=True)
    
    # Request metrics
    request_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    avg_latency_ms = models.FloatField(default=0.0)
    p50_latency_ms = models.FloatField(default=0.0)
    p95_latency_ms = models.FloatField(default=0.0)
    p99_latency_ms = models.FloatField(default=0.0)
    
    # Throughput
    requests_per_second = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Application Metric'
        verbose_name_plural = 'Application Metrics'
        indexes = [
            models.Index(fields=['app_name', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.app_name} - {self.request_count} requests"

    @property
    def error_rate(self):
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100


class EndpointMetric(BaseModel, ObservabilityMixin):
    """Per-endpoint performance metrics."""
    app_name = models.CharField(max_length=255, db_index=True)
    endpoint = models.CharField(max_length=500, db_index=True)
    method = models.CharField(max_length=10)  # GET, POST, etc.
    
    request_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    avg_latency_ms = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Endpoint Metric'
        verbose_name_plural = 'Endpoint Metrics'
        indexes = [
            models.Index(fields=['app_name', 'endpoint', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.method} {self.endpoint}"
