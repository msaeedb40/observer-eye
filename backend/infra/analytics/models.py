"""
Analytics models for Observer-Eye Platform.
BI analytics and data analysis.
"""
from django.db import models
from core.models import BaseModel


class Dashboard(BaseModel):
    """Custom analytics dashboard."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    layout = models.JSONField(default=dict)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'

    def __str__(self):
        return self.name


class Widget(BaseModel):
    """Dashboard widget."""
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    name = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=50)  # chart, table, metric, etc.
    config = models.JSONField(default=dict)
    position = models.JSONField(default=dict)  # x, y, width, height
    data_source = models.CharField(max_length=255)
    query = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'

    def __str__(self):
        return f"{self.name} ({self.widget_type})"


class Report(BaseModel):
    """Analytics report."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=50)
    query = models.JSONField(default=dict)
    schedule = models.CharField(max_length=100, blank=True)  # cron expression
    recipients = models.JSONField(default=list)
    last_run = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        return self.name


class SavedQuery(BaseModel):
    """Saved analytics query."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    data_source = models.CharField(max_length=255)
    query = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = 'Saved Query'
        verbose_name_plural = 'Saved Queries'

    def __str__(self):
        return self.name
