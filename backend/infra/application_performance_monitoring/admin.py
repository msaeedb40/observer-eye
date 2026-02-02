"""APM admin."""
from django.contrib import admin
from .models import APMTransaction, APMSpan, APMError

@admin.register(APMTransaction)
class APMTransactionAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'transaction_name', 'duration_ms', 'result', 'http_status_code', 'timestamp']
    list_filter = ['app_name', 'result']
    search_fields = ['transaction_name']
    ordering = ['-timestamp']

@admin.register(APMSpan)
class APMSpanAdmin(admin.ModelAdmin):
    list_display = ['name', 'span_type', 'duration_ms', 'transaction']
    list_filter = ['span_type']
    ordering = ['-created_at']

@admin.register(APMError)
class APMErrorAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'error_type', 'message_preview', 'handled', 'count', 'timestamp']
    list_filter = ['app_name', 'handled']
    search_fields = ['error_type', 'message']
    ordering = ['-timestamp']

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
