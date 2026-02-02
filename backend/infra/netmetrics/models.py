"""
Network Metrics models for Observer-Eye Platform.
Tracks network-level metrics: bandwidth, latency, packet loss.
"""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class NetworkMetric(BaseModel, ObservabilityMixin):
    """Network-level metrics."""
    host = models.CharField(max_length=255, db_index=True)
    interface = models.CharField(max_length=100, db_index=True)
    
    # Bandwidth
    bytes_sent = models.BigIntegerField(default=0)
    bytes_received = models.BigIntegerField(default=0)
    packets_sent = models.BigIntegerField(default=0)
    packets_received = models.BigIntegerField(default=0)
    
    # Errors
    errors_in = models.IntegerField(default=0)
    errors_out = models.IntegerField(default=0)
    drops_in = models.IntegerField(default=0)
    drops_out = models.IntegerField(default=0)
    
    # Latency
    latency_ms = models.FloatField(default=0.0)
    jitter_ms = models.FloatField(default=0.0)
    packet_loss_percent = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Network Metric'
        verbose_name_plural = 'Network Metrics'
        indexes = [
            models.Index(fields=['host', 'interface', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.host}:{self.interface}"


class ConnectionMetric(BaseModel, ObservabilityMixin):
    """Connection-level metrics."""
    host = models.CharField(max_length=255, db_index=True)
    active_connections = models.IntegerField(default=0)
    established_connections = models.IntegerField(default=0)
    time_wait_connections = models.IntegerField(default=0)
    close_wait_connections = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Connection Metric'
        verbose_name_plural = 'Connection Metrics'

    def __str__(self):
        return f"{self.host} - {self.active_connections} active"
