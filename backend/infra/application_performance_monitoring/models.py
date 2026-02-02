"""
Application Performance Monitoring (APM) models.
Tracks application performance: latency, throughput, errors.
"""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class APMTransaction(BaseModel, ObservabilityMixin):
    """APM Transaction - represents a single request/operation."""
    app_name = models.CharField(max_length=255, db_index=True)
    transaction_name = models.CharField(max_length=500, db_index=True)
    transaction_type = models.CharField(max_length=100, default='request')
    
    # Timing
    duration_ms = models.FloatField()
    cpu_time_ms = models.FloatField(default=0.0)
    
    # Result
    result = models.CharField(max_length=50, default='success')  # success, error
    outcome = models.CharField(max_length=50, blank=True)
    
    # HTTP specific
    http_method = models.CharField(max_length=10, blank=True)
    http_status_code = models.IntegerField(null=True, blank=True)
    http_url = models.CharField(max_length=2000, blank=True)
    
    # Trace correlation
    trace_id = models.CharField(max_length=64, blank=True, db_index=True)
    span_id = models.CharField(max_length=32, blank=True)
    
    class Meta:
        verbose_name = 'APM Transaction'
        verbose_name_plural = 'APM Transactions'
        indexes = [
            models.Index(fields=['app_name', 'transaction_name', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.transaction_name} - {self.duration_ms}ms"


class APMSpan(BaseModel):
    """APM Span - represents a single operation within a transaction."""
    transaction = models.ForeignKey(APMTransaction, on_delete=models.CASCADE, related_name='spans')
    name = models.CharField(max_length=500)
    span_type = models.CharField(max_length=100)  # db, http, custom
    
    duration_ms = models.FloatField()
    start_offset_ms = models.FloatField(default=0.0)
    
    # Database specific
    db_type = models.CharField(max_length=50, blank=True)
    db_statement = models.TextField(blank=True)
    
    # HTTP specific
    http_url = models.CharField(max_length=2000, blank=True)
    http_status_code = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'APM Span'
        verbose_name_plural = 'APM Spans'

    def __str__(self):
        return f"{self.name} ({self.span_type})"


class APMError(BaseModel, ObservabilityMixin):
    """APM Error - tracked errors."""
    app_name = models.CharField(max_length=255, db_index=True)
    error_type = models.CharField(max_length=255, db_index=True)
    message = models.TextField()
    stack_trace = models.TextField(blank=True)
    
    transaction_name = models.CharField(max_length=500, blank=True)
    trace_id = models.CharField(max_length=64, blank=True, db_index=True)
    
    handled = models.BooleanField(default=True)
    count = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = 'APM Error'
        verbose_name_plural = 'APM Errors'

    def __str__(self):
        return f"{self.error_type}: {self.message[:50]}"
