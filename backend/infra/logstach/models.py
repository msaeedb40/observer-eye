from django.db import models
from core.models import BaseModel


class LogPipeline(BaseModel):
    """Configuration for log data routing."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    source_type = models.CharField(
        max_length=50, 
        choices=[('file', 'File'), ('tcp', 'TCP'), ('udp', 'UDP'), ('syslog', 'Syslog')],
        default='tcp'
    )
    port = models.IntegerField(default=514)
    
    # Processing
    parsers = models.JSONField(default=list, blank=True)  # e.g. ['json', 'grok']
    
    # Output
    destination_type = models.CharField(
        max_length=50,
        choices=[('elasticsearch', 'Elasticsearch'), ('s3', 'S3 Bucket'), ('stdout', 'Console')],
        default='elasticsearch'
    )
    destination_config = models.JSONField(default=dict, blank=True)
    
    enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Log Pipeline'
        verbose_name_plural = 'Log Pipelines'

    def __str__(self):
        return f"{self.name} ({self.source_type} -> {self.destination_type})"


class SanitizationRule(BaseModel):
    """Rule for masking sensitive data in logs."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    pattern_type = models.CharField(
        max_length=20,
        choices=[('regex', 'Regex Pattern'), ('keyword', 'Exact Keyword')],
        default='regex'
    )
    pattern = models.CharField(max_length=500)  # The regex or keyword to match
    replacement = models.CharField(max_length=100, default='***REDACTED***')
    
    # Scope
    apply_to_pipelines = models.ManyToManyField(LogPipeline, blank=True)
    is_global = models.BooleanField(default=False)  # Apply to all
    
    enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Sanitization Rule'
        verbose_name_plural = 'Sanitization Rules'

    def __str__(self):
        return self.name
