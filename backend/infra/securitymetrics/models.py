"""
Security Metrics models for Observer-Eye Platform.
Tracks security-related metrics: auth attempts, threats, compliance.
"""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class SecurityMetric(BaseModel, ObservabilityMixin):
    """Security-level metrics."""
    host = models.CharField(max_length=255, db_index=True)
    
    # Authentication
    auth_attempts = models.IntegerField(default=0)
    auth_failures = models.IntegerField(default=0)
    auth_successes = models.IntegerField(default=0)
    
    # Threats
    blocked_requests = models.IntegerField(default=0)
    suspicious_activities = models.IntegerField(default=0)
    
    # Compliance
    policy_violations = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Security Metric'
        verbose_name_plural = 'Security Metrics'
        indexes = [
            models.Index(fields=['host', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.host} - {self.auth_attempts} auth attempts"

    @property
    def auth_failure_rate(self):
        if self.auth_attempts == 0:
            return 0.0
        return (self.auth_failures / self.auth_attempts) * 100


class ThreatEvent(BaseModel, ObservabilityMixin):
    """Detected security threats."""
    host = models.CharField(max_length=255, db_index=True)
    threat_type = models.CharField(max_length=100, db_index=True)
    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        db_index=True
    )
    description = models.TextField()
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    blocked = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Threat Event'
        verbose_name_plural = 'Threat Events'

    def __str__(self):
        return f"{self.threat_type} ({self.severity})"


class AuditLog(BaseModel):
    """Audit log for compliance tracking."""
    user = models.CharField(max_length=255, db_index=True)
    action = models.CharField(max_length=100, db_index=True)
    resource = models.CharField(max_length=255)
    resource_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=True)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} on {self.resource}"
