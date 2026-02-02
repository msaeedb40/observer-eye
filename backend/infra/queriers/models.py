"""
Queriers models for Observer-Eye Platform.
Data query engines for metrics, logs, and traces.
"""
from django.db import models
from core.models import BaseModel


class QueryTemplate(BaseModel):
    """Saved query template."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    data_type = models.CharField(
        max_length=50,
        choices=[
            ('metrics', 'Metrics'),
            ('logs', 'Logs'),
            ('traces', 'Traces'),
            ('events', 'Events'),
        ],
        db_index=True
    )
    query_language = models.CharField(max_length=50, default='json')  # json, promql, sql
    template = models.TextField()
    parameters = models.JSONField(default=list, blank=True)  # List of parameter definitions
    
    class Meta:
        verbose_name = 'Query Template'
        verbose_name_plural = 'Query Templates'

    def __str__(self):
        return self.name


class QueryExecution(BaseModel):
    """Query execution history."""
    template = models.ForeignKey(QueryTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.CharField(max_length=255, db_index=True)
    query = models.TextField()
    data_type = models.CharField(max_length=50)
    parameters = models.JSONField(default=dict, blank=True)
    
    # Execution stats
    executed_at = models.DateTimeField(auto_now_add=True, db_index=True)
    duration_ms = models.FloatField(null=True, blank=True)
    row_count = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, running, success, error
    error_message = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Query Execution'
        verbose_name_plural = 'Query Executions'
        ordering = ['-executed_at']

    def __str__(self):
        return f"Query {self.id} ({self.status})"
