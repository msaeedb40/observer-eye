"""
Settings models for Observer-Eye Platform.
Platform configuration management.
"""
from django.db import models
from core.models import BaseModel


class Setting(BaseModel):
    """Platform settings."""
    key = models.CharField(max_length=255, unique=True, db_index=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default='general', db_index=True)
    is_sensitive = models.BooleanField(default=False)  # Mask in UI
    
    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.key


class UserPreference(BaseModel):
    """User-specific preferences."""
    user_id = models.CharField(max_length=255, db_index=True)
    key = models.CharField(max_length=255)
    value = models.JSONField()
    
    class Meta:
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'
        unique_together = ['user_id', 'key']

    def __str__(self):
        return f"{self.user_id}:{self.key}"


class FeatureFlag(BaseModel):
    """Feature flag configuration."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    rollout_percentage = models.IntegerField(default=0)  # 0-100
    conditions = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Feature Flag'
        verbose_name_plural = 'Feature Flags'

    def __str__(self):
        return f"{self.name} ({'enabled' if self.enabled else 'disabled'})"


class WorkspaceSettings(BaseModel):
    """Workspace-level settings (tenant/org)."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    # Quotas
    total_metrics_limit = models.BigIntegerField(default=10000000)  # max data points
    total_logs_limit_gb = models.FloatField(default=100.0)
    retention_days = models.IntegerField(default=30)
    
    # Features
    ai_enabled = models.BooleanField(default=True)
    custom_dashboards_limit = models.IntegerField(default=50)
    
    class Meta:
        verbose_name = 'Workspace Settings'
        verbose_name_plural = 'Workspace Settings'

    def __str__(self):
        return self.name
