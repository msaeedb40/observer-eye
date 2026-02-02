"""Identity Performance Monitoring admin."""
from django.contrib import admin
from .models import IdentityPerformance

@admin.register(IdentityPerformance)
class IdentityPerformanceAdmin(admin.ModelAdmin):
    list_display = ['auth_type', 'provider', 'execution_time_ms', 'success', 'timestamp']
    list_filter = ['auth_type', 'success']
