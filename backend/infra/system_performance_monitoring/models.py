"""System Performance Monitoring models."""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class SystemPerformance(BaseModel, ObservabilityMixin):
    """System-level performance metrics."""
    host = models.CharField(max_length=255, db_index=True)
    operation_type = models.CharField(max_length=100, db_index=True)  # io, memory, cpu
    execution_time_ms = models.FloatField()
    resource_utilization = models.FloatField(default=0.0)  # percentage
    
    class Meta:
        verbose_name = 'System Performance'
        verbose_name_plural = 'System Performance'

    def __str__(self):
        return f"{self.host}:{self.operation_type} - {self.execution_time_ms}ms"
