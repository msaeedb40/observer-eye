"""Analytics Performance Monitoring models."""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class AnalyticsPerformance(BaseModel, ObservabilityMixin):
    """Analytics system performance metrics."""
    query_type = models.CharField(max_length=100, db_index=True)
    execution_time_ms = models.FloatField()
    rows_processed = models.IntegerField(default=0)
    cache_hit = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Analytics Performance'
        verbose_name_plural = 'Analytics Performance'

    def __str__(self):
        return f"{self.query_type}: {self.execution_time_ms}ms"
