"""
Core serializers for Observer-Eye Platform.
"""
from rest_framework import serializers
from .models import Metric, Event, LogEntry, Trace, Span


class MetricSerializer(serializers.ModelSerializer):
    """Serializer for Metric model."""
    
    class Meta:
        model = Metric
        fields = [
            'id', 'name', 'value', 'unit', 'metric_type',
            'source', 'timestamp', 'labels', 'metadata',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""
    
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'event_type', 'data', 'severity',
            'source', 'timestamp', 'labels', 'metadata',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']


class LogEntrySerializer(serializers.ModelSerializer):
    """Serializer for LogEntry model."""
    
    class Meta:
        model = LogEntry
        fields = [
            'id', 'level', 'message', 'logger_name',
            'trace_id', 'span_id', 'source', 'timestamp',
            'labels', 'metadata', 'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']


class SpanSerializer(serializers.ModelSerializer):
    """Serializer for Span model."""
    
    class Meta:
        model = Span
        fields = [
            'id', 'span_id', 'parent_span_id', 'name',
            'start_time', 'end_time', 'duration_ms',
            'status', 'attributes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'duration_ms']


class TraceSerializer(serializers.ModelSerializer):
    """Serializer for Trace model with nested spans."""
    spans = SpanSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trace
        fields = [
            'id', 'trace_id', 'name', 'service_name',
            'start_time', 'end_time', 'duration_ms',
            'status', 'attributes', 'spans', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'duration_ms']


class TraceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Trace listing."""
    span_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Trace
        fields = [
            'id', 'trace_id', 'name', 'service_name',
            'start_time', 'duration_ms', 'status', 'span_count'
        ]
    
    def get_span_count(self, obj):
        return obj.spans.count()
