"""
Core models for Observer-Eye Platform.
Base models with audit fields and observability mixins.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """
    Abstract base model with audit fields.
    All Observer apps should inherit from this.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(app_label)s_%(class)s_created'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class ObservabilityMixin(models.Model):
    """
    Mixin for observability data with common fields.
    Implements the 4 pillars: Metrics, Events, Logs, Traces.
    """
    source = models.CharField(max_length=255, db_index=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    labels = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        abstract = True


class Metric(BaseModel, ObservabilityMixin):
    """
    Metric model - Pillar 1 of Observability.
    Stores numerical measurements over time.
    """
    name = models.CharField(max_length=255, db_index=True)
    value = models.FloatField(default=0.0, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    metric_type = models.CharField(
        max_length=20,
        choices=[
            ('counter', 'Counter'),
            ('gauge', 'Gauge'),
            ('histogram', 'Histogram'),
            ('summary', 'Summary'),
        ],
        default='gauge'
    )

    class Meta:
        verbose_name = 'Metric'
        verbose_name_plural = 'Metrics'
        indexes = [
            models.Index(fields=['name', 'timestamp']),
            models.Index(fields=['source', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.name}: {self.value} ({self.source})"


class Event(BaseModel, ObservabilityMixin):
    """
    Event model - Pillar 2 of Observability.
    Stores discrete occurrences with context.
    """
    name = models.CharField(max_length=255, db_index=True)
    event_type = models.CharField(max_length=100, db_index=True)
    data = models.JSONField(default=dict)
    severity = models.CharField(
        max_length=20,
        choices=[
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('critical', 'Critical'),
        ],
        default='info'
    )

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['name', 'timestamp']),
            models.Index(fields=['event_type', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.name} ({self.event_type})"


class LogEntry(BaseModel, ObservabilityMixin):
    """
    Log Entry model - Pillar 3 of Observability.
    Stores timestamped text records.
    """
    level = models.CharField(
        max_length=20,
        choices=[
            ('debug', 'Debug'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('critical', 'Critical'),
        ],
        db_index=True
    )
    message = models.TextField()
    logger_name = models.CharField(max_length=255, blank=True)
    trace_id = models.CharField(max_length=64, blank=True, db_index=True)
    span_id = models.CharField(max_length=32, blank=True)

    class Meta:
        verbose_name = 'Log Entry'
        verbose_name_plural = 'Log Entries'
        indexes = [
            models.Index(fields=['level', 'timestamp']),
            models.Index(fields=['source', 'level']),
        ]

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"


class Trace(BaseModel):
    """
    Trace model - Pillar 4 of Observability.
    Stores request flow across services.
    """
    trace_id = models.CharField(max_length=64, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255, db_index=True)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_ms = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('ok', 'OK'),
            ('error', 'Error'),
            ('unset', 'Unset'),
        ],
        default='unset'
    )
    attributes = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Trace'
        verbose_name_plural = 'Traces'

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            self.duration_ms = delta.total_seconds() * 1000
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.trace_id[:8]})"


class Span(BaseModel):
    """
    Span model - Part of Trace (Pillar 4).
    Individual operation within a trace.
    """
    trace = models.ForeignKey(Trace, on_delete=models.CASCADE, related_name='spans')
    span_id = models.CharField(max_length=32, db_index=True)
    parent_span_id = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration_ms = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, default='unset')
    attributes = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Span'
        verbose_name_plural = 'Spans'
        unique_together = ['trace', 'span_id']

    def __str__(self):
        return f"{self.name} ({self.span_id[:8]})"
