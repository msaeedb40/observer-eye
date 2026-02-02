"""Security Performance Monitoring admin."""
from django.contrib import admin
from .models import SecurityPerformance

@admin.register(SecurityPerformance)
class SecurityPerformanceAdmin(admin.ModelAdmin):
    list_display = ['operation_type', 'execution_time_ms', 'threats_detected', 'timestamp']
    list_filter = ['operation_type']
