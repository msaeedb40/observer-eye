"""Analytics Performance Monitoring admin."""
from django.contrib import admin
from .models import AnalyticsPerformance

@admin.register(AnalyticsPerformance)
class AnalyticsPerformanceAdmin(admin.ModelAdmin):
    list_display = ['query_type', 'execution_time_ms', 'cache_hit', 'timestamp']
    list_filter = ['query_type', 'cache_hit']
