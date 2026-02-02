"""System Metrics admin."""
from django.contrib import admin
from .models import SystemMetric, DiskMetric, ProcessMetric

@admin.register(SystemMetric)
class SystemMetricAdmin(admin.ModelAdmin):
    list_display = ['host', 'cpu_percent', 'memory_percent', 'load_avg_1min', 'timestamp']
    list_filter = ['host']
    search_fields = ['host', 'hostname']
    ordering = ['-timestamp']

@admin.register(DiskMetric)
class DiskMetricAdmin(admin.ModelAdmin):
    list_display = ['host', 'mount_point', 'usage_percent', 'timestamp']
    list_filter = ['host']
    ordering = ['-timestamp']

@admin.register(ProcessMetric)
class ProcessMetricAdmin(admin.ModelAdmin):
    list_display = ['host', 'name', 'pid', 'cpu_percent', 'memory_percent', 'timestamp']
    list_filter = ['host', 'status']
    search_fields = ['name']
    ordering = ['-cpu_percent']
