"""
Insights Observer models for Observer-Eye Platform.
AI-powered insights and recommendations.
"""
from django.db import models
from core.models import BaseModel


class Insight(BaseModel):
    """AI-generated insight."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    insight_type = models.CharField(
        max_length=50,
        choices=[
            ('anomaly', 'Anomaly Detection'),
            ('trend', 'Trend Analysis'),
            ('recommendation', 'Recommendation'),
            ('alert', 'Alert Correlation'),
            ('capacity', 'Capacity Planning'),
        ],
        db_index=True
    )
    severity = models.CharField(
        max_length=20,
        choices=[
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('critical', 'Critical'),
        ],
        default='info'
    )
    
    # Source data
    data_source = models.CharField(max_length=255)
    related_entities = models.JSONField(default=list, blank=True)  # services, hosts, etc.
    evidence = models.JSONField(default=dict, blank=True)  # supporting data
    
    # Recommendations
    recommendations = models.JSONField(default=list, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('acknowledged', 'Acknowledged'),
            ('resolved', 'Resolved'),
            ('dismissed', 'Dismissed'),
        ],
        default='new',
        db_index=True
    )
    
    class Meta:
        verbose_name = 'Insight'
        verbose_name_plural = 'Insights'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AnomalyDetection(BaseModel):
    """Anomaly detection result."""
    metric_name = models.CharField(max_length=255, db_index=True)
    source = models.CharField(max_length=255, db_index=True)
    
    expected_value = models.FloatField()
    actual_value = models.FloatField()
    deviation_score = models.FloatField()
    
    detected_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Anomaly Detection'
        verbose_name_plural = 'Anomaly Detections'
        ordering = ['-detected_at']

    def __str__(self):
        return f"Anomaly: {self.metric_name} ({self.deviation_score:.2f})"
