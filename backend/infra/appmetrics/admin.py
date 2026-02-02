"""Application Metrics admin."""
from django.contrib import admin
from .models import ApplicationMetric, EndpointMetric


@admin.register(ApplicationMetric)
class ApplicationMetricAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'environment', 'request_count', 'error_count', 'avg_latency_ms', 'timestamp']
    list_filter = ['app_name', 'environment']
    search_fields = ['app_name']
    ordering = ['-timestamp']


@admin.register(EndpointMetric)
class EndpointMetricAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'method', 'endpoint', 'request_count', 'avg_latency_ms', 'timestamp']
    list_filter = ['app_name', 'method']
    search_fields = ['endpoint']
    ordering = ['-timestamp']
