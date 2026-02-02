"""Security Metrics admin."""
from django.contrib import admin
from .models import SecurityMetric, ThreatEvent, AuditLog

@admin.register(SecurityMetric)
class SecurityMetricAdmin(admin.ModelAdmin):
    list_display = ['host', 'auth_attempts', 'auth_failures', 'blocked_requests', 'timestamp']
    list_filter = ['host']
    ordering = ['-timestamp']

@admin.register(ThreatEvent)
class ThreatEventAdmin(admin.ModelAdmin):
    list_display = ['threat_type', 'severity', 'host', 'blocked', 'timestamp']
    list_filter = ['threat_type', 'severity', 'blocked']
    search_fields = ['description']
    ordering = ['-timestamp']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'resource', 'success', 'ip_address', 'timestamp']
    list_filter = ['action', 'success']
    search_fields = ['user', 'resource']
    ordering = ['-timestamp']
