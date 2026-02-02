"""Identity Performance Monitoring models."""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class IdentityPerformance(BaseModel, ObservabilityMixin):
    """Identity/auth system performance metrics."""
    auth_type = models.CharField(max_length=100, db_index=True)  # login, token_refresh, oauth
    provider = models.CharField(max_length=100, blank=True)
    execution_time_ms = models.FloatField()
    success = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Identity Performance'
        verbose_name_plural = 'Identity Performance'

    def __str__(self):
        return f"{self.auth_type}: {self.execution_time_ms}ms"
