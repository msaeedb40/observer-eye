"""Admin configuration for Core app."""
from django.contrib import admin
from .models import Metric, Event, LogEntry, Trace, Span


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'unit', 'metric_type', 'source', 'timestamp']
    list_filter = ['metric_type', 'source', 'timestamp']
    search_fields = ['name', 'source']
    ordering = ['-timestamp']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'severity', 'source', 'timestamp']
    list_filter = ['event_type', 'severity', 'source']
    search_fields = ['name', 'event_type']
    ordering = ['-timestamp']


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['level', 'message_preview', 'source', 'trace_id', 'timestamp']
    list_filter = ['level', 'source']
    search_fields = ['message', 'source', 'trace_id']
    ordering = ['-timestamp']

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


@admin.register(Trace)
class TraceAdmin(admin.ModelAdmin):
    list_display = ['trace_id', 'name', 'service_name', 'duration_ms', 'status', 'start_time']
    list_filter = ['status', 'service_name']
    search_fields = ['trace_id', 'name', 'service_name']
    ordering = ['-start_time']


@admin.register(Span)
class SpanAdmin(admin.ModelAdmin):
    list_display = ['span_id', 'name', 'trace', 'duration_ms', 'status', 'start_time']
    list_filter = ['status']
    search_fields = ['span_id', 'name']
    ordering = ['-start_time']
