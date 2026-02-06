"""
Synthetic Monitoring models for Observer-Eye Platform.
Tracks automated checks, uptime, and performance from external locations.
"""
from django.db import models
from core.models import BaseModel


class SyntheticMonitor(BaseModel):
    """Synthetic monitoring configuration."""
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=2048)
    check_type = models.CharField(
        max_length=50,
        choices=[
            ('http', 'HTTP/HTTPS'),
            ('ssl', 'SSL/TLS Certificate'),
            ('dns', 'DNS Resolution'),
            ('tcp', 'TCP Port'),
            ('ping', 'ICMP Ping'),
            ('browser', 'Managed Browser'),
        ],
        default='http'
    )
    
    method = models.CharField(
        max_length=10,
        choices=[
            ('GET', 'GET'),
            ('POST', 'POST'),
            ('PUT', 'PUT'),
            ('DELETE', 'DELETE'),
            ('HEAD', 'HEAD'),
        ],
        default='GET'
    )
    
    headers = models.JSONField(default=dict, blank=True)
    body = models.TextField(blank=True)
    
    interval_seconds = models.IntegerField(default=60)
    timeout_seconds = models.IntegerField(default=30)
    locations = models.JSONField(default=list)  # List of geographic locations
    
    assertions = models.JSONField(default=list)  # Response expectations
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Synthetic Monitor'
        verbose_name_plural = 'Synthetic Monitors'

    def __str__(self):
        return f"{self.name} ({self.check_type})"


class SyntheticResult(BaseModel):
    """Synthetic check result."""
    monitor = models.ForeignKey(SyntheticMonitor, on_delete=models.CASCADE, related_name='results')
    location = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('failure', 'Failure'),
            ('timeout', 'Timeout'),
            ('error', 'Script Error'),
        ],
        db_index=True
    )
    
    # Timing
    response_time_ms = models.FloatField()
    dns_time_ms = models.FloatField(null=True, blank=True)
    connect_time_ms = models.FloatField(null=True, blank=True)
    tls_time_ms = models.FloatField(null=True, blank=True)
    ttfb_ms = models.FloatField(null=True, blank=True)
    download_time_ms = models.FloatField(null=True, blank=True)
    
    # Details
    http_status_code = models.IntegerField(null=True, blank=True)
    body_size_bytes = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Evidence
    screenshot_url = models.URLField(max_length=2048, blank=True)
    trace_id = models.CharField(max_length=64, blank=True)
    
    class Meta:
        verbose_name = 'Synthetic Result'
        verbose_name_plural = 'Synthetic Results'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.monitor.name} from {self.location}: {self.status}"
