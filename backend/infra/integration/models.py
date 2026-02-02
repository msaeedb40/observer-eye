"""
Integration models for Observer-Eye Platform.
Third-party integrations and data sources.
"""
from django.db import models
from core.models import BaseModel


class Integration(BaseModel):
    """Third-party integration configuration."""
    name = models.CharField(max_length=255)
    integration_type = models.CharField(
        max_length=50,
        choices=[
            ('prometheus', 'Prometheus'),
            ('grafana', 'Grafana'),
            ('elasticsearch', 'Elasticsearch'),
            ('jaeger', 'Jaeger'),
            ('datadog', 'Datadog'),
            ('newrelic', 'New Relic'),
            ('aws', 'AWS CloudWatch'),
            ('gcp', 'GCP Operations'),
            ('azure', 'Azure Monitor'),
            ('custom', 'Custom'),
        ],
        db_index=True
    )
    description = models.TextField(blank=True)
    
    # Connection
    endpoint_url = models.URLField(max_length=500)
    auth_type = models.CharField(
        max_length=20,
        choices=[
            ('none', 'None'),
            ('basic', 'Basic Auth'),
            ('bearer', 'Bearer Token'),
            ('api_key', 'API Key'),
            ('oauth2', 'OAuth 2.0'),
        ],
        default='none'
    )
    credentials = models.JSONField(default=dict, blank=True)  # Encrypted in production
    
    # Status
    enabled = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_status = models.CharField(max_length=50, default='pending')
    
    class Meta:
        verbose_name = 'Integration'
        verbose_name_plural = 'Integrations'

    def __str__(self):
        return f"{self.name} ({self.integration_type})"


class DataSource(BaseModel):
    """Data source for metrics collection."""
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='data_sources', null=True, blank=True)
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=50)  # metrics, logs, traces
    config = models.JSONField(default=dict)
    polling_interval = models.IntegerField(default=60)  # seconds
    enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'

    def __str__(self):
        return self.name


class Webhook(BaseModel):
    """Incoming webhook for data ingestion."""
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=64, unique=True)  # Authentication token
    data_type = models.CharField(max_length=50)  # metrics, logs, events
    enabled = models.BooleanField(default=True)
    last_received = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Webhook'
        verbose_name_plural = 'Webhooks'

    def __str__(self):
        return self.name
