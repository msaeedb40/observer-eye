"""Traffic Performance Monitoring admin."""
from django.contrib import admin
from .models import TrafficPerformance

@admin.register(TrafficPerformance)
class TrafficPerformanceAdmin(admin.ModelAdmin):
    list_display = ['host', 'requests_per_second', 'avg_latency_ms', 'error_rate', 'timestamp']
    list_filter = ['host']
