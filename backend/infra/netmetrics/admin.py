"""Network Metrics admin."""
from django.contrib import admin
from .models import NetworkMetric, ConnectionMetric

@admin.register(NetworkMetric)
class NetworkMetricAdmin(admin.ModelAdmin):
    list_display = ['host', 'interface', 'bytes_sent', 'bytes_received', 'latency_ms', 'timestamp']
    list_filter = ['host', 'interface']
    search_fields = ['host']
    ordering = ['-timestamp']

@admin.register(ConnectionMetric)
class ConnectionMetricAdmin(admin.ModelAdmin):
    list_display = ['host', 'active_connections', 'established_connections', 'timestamp']
    list_filter = ['host']
    ordering = ['-timestamp']
