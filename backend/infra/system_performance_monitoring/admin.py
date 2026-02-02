"""System Performance Monitoring admin."""
from django.contrib import admin
from .models import SystemPerformance

@admin.register(SystemPerformance)
class SystemPerformanceAdmin(admin.ModelAdmin):
    list_display = ['host', 'operation_type', 'execution_time_ms', 'resource_utilization', 'timestamp']
    list_filter = ['host', 'operation_type']
