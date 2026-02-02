"""Traffic Performance Monitoring models."""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class TrafficPerformance(BaseModel, ObservabilityMixin):
    """Traffic/network performance metrics."""
    host = models.CharField(max_length=255, db_index=True)
    endpoint = models.CharField(max_length=500, blank=True)
    
    requests_per_second = models.FloatField(default=0.0)
    bytes_per_second = models.FloatField(default=0.0)
    avg_latency_ms = models.FloatField(default=0.0)
    error_rate = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Traffic Performance'
        verbose_name_plural = 'Traffic Performance'

    def __str__(self):
        return f"{self.host}: {self.requests_per_second} rps"
