"""Insights Observer admin."""
from django.contrib import admin
from .models import Insight, AnomalyDetection

@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'insight_type', 'severity', 'status', 'created_at']
    list_filter = ['insight_type', 'severity', 'status']
    search_fields = ['title']

@admin.register(AnomalyDetection)
class AnomalyDetectionAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'source', 'deviation_score', 'is_resolved', 'detected_at']
    list_filter = ['source', 'is_resolved']
    ordering = ['-detected_at']
