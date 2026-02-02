"""Security Performance Monitoring models."""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class SecurityPerformance(BaseModel, ObservabilityMixin):
    """Security system performance metrics."""
    operation_type = models.CharField(max_length=100, db_index=True)  # scan, validation, encryption
    execution_time_ms = models.FloatField()
    items_processed = models.IntegerField(default=0)
    threats_detected = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Security Performance'
        verbose_name_plural = 'Security Performance'

    def __str__(self):
        return f"{self.operation_type}: {self.execution_time_ms}ms"
