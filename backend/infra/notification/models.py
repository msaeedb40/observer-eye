"""
Notification models for Observer-Eye Platform.
Alert and notification system.
"""
from django.db import models
from core.models import BaseModel


class NotificationChannel(BaseModel):
    """Notification delivery channel."""
    name = models.CharField(max_length=255)
    channel_type = models.CharField(
        max_length=50,
        choices=[
            ('email', 'Email'),
            ('slack', 'Slack'),
            ('webhook', 'Webhook'),
            ('pagerduty', 'PagerDuty'),
            ('teams', 'Microsoft Teams'),
            ('sms', 'SMS'),
        ],
        db_index=True
    )
    config = models.JSONField(default=dict)  # channel-specific configuration
    is_default = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Notification Channel'
        verbose_name_plural = 'Notification Channels'

    def __str__(self):
        return f"{self.name} ({self.channel_type})"


class AlertRule(BaseModel):
    """Alert rule definition."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Condition
    data_source = models.CharField(max_length=255)  # metrics, logs, etc.
    condition_type = models.CharField(max_length=50)  # threshold, anomaly, etc.
    condition = models.JSONField(default=dict)  # query and threshold
    
    # Severity
    severity = models.CharField(
        max_length=20,
        choices=[
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('critical', 'Critical'),
        ],
        default='warning'
    )
    
    # Notification
    channels = models.ManyToManyField(NotificationChannel, blank=True)
    
    # Timing
    evaluation_interval = models.IntegerField(default=60)  # seconds
    for_duration = models.IntegerField(default=0)  # seconds before alert fires
    
    enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Alert Rule'
        verbose_name_plural = 'Alert Rules'

    def __str__(self):
        return self.name


class Alert(BaseModel):
    """Triggered alert instance."""
    rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    condition = models.CharField(max_length=500, blank=True)  # Allow direct condition on standalone alerts
    
    state = models.CharField(
        max_length=20,
        choices=[
            ('firing', 'Firing'),
            ('resolved', 'Resolved'),
            ('acknowledged', 'Acknowledged'),
            ('silenced', 'Silenced'),
        ],
        default='firing',
        db_index=True
    )
    severity = models.CharField(max_length=20, db_index=True, default='warning')
    message = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)
    
    # Dispatch channels for standalone alerts
    dispatch_channels = models.JSONField(default=list, blank=True)  # ["email", "slack"]
    email_config = models.JSONField(default=dict, blank=True)
    slack_config = models.JSONField(default=dict, blank=True)
    
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    event_start_at = models.DateTimeField(null=True, blank=True, db_index=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.CharField(max_length=255, blank=True)
    
    annotations = models.JSONField(default=dict, blank=True)
    labels = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.name} ({self.state})"


class NotificationHistory(BaseModel):
    """Notification delivery history."""
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='notifications')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.SET_NULL, null=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Notification History'
        verbose_name_plural = 'Notification History'

    def __str__(self):
        return f"{self.alert.name} -> {self.channel.name if self.channel else 'N/A'}"
