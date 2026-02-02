"""
Core views for Observer-Eye Platform.
REST API endpoints for the 4 pillars of observability.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from .models import Metric, Event, LogEntry, Trace, Span
from .serializers import (
    MetricSerializer, EventSerializer, LogEntrySerializer,
    TraceSerializer, TraceListSerializer, SpanSerializer
)


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'observer-eye-backend',
        'version': '1.0.0'
    })


class MetricViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Metric model (Pillar 1).
    Provides CRUD operations for metrics.
    """
    queryset = Metric.objects.filter(is_active=True)
    serializer_class = MetricSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'source', 'metric_type']
    search_fields = ['name', 'source']
    ordering_fields = ['timestamp', 'name', 'value']
    ordering = ['-timestamp']

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple metrics at once."""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'created', 'count': len(serializer.data)}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get metrics summary."""
        total = self.get_queryset().count()
        by_type = {}
        for mt in ['counter', 'gauge', 'histogram', 'summary']:
            by_type[mt] = self.get_queryset().filter(metric_type=mt).count()
        return Response({'total': total, 'by_type': by_type})


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event model (Pillar 2).
    Provides CRUD operations for events.
    """
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'event_type', 'severity', 'source']
    search_fields = ['name', 'event_type']
    ordering_fields = ['timestamp', 'severity']
    ordering = ['-timestamp']

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple events at once."""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'created', 'count': len(serializer.data)}, status=status.HTTP_201_CREATED)


class LogEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for LogEntry model (Pillar 3).
    Provides CRUD operations for log entries.
    """
    queryset = LogEntry.objects.filter(is_active=True)
    serializer_class = LogEntrySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'source', 'trace_id']
    search_fields = ['message', 'source', 'logger_name']
    ordering_fields = ['timestamp', 'level']
    ordering = ['-timestamp']

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple log entries at once."""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'created', 'count': len(serializer.data)}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def by_trace(self, request):
        """Get logs by trace ID."""
        trace_id = request.query_params.get('trace_id')
        if not trace_id:
            return Response({'error': 'trace_id required'}, status=400)
        logs = self.get_queryset().filter(trace_id=trace_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)


class TraceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trace model (Pillar 4).
    Provides CRUD operations for traces with nested spans.
    """
    queryset = Trace.objects.filter(is_active=True).prefetch_related('spans')
    serializer_class = TraceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['service_name', 'status']
    search_fields = ['name', 'trace_id', 'service_name']
    ordering_fields = ['start_time', 'duration_ms']
    ordering = ['-start_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return TraceListSerializer
        return TraceSerializer

    @action(detail=True, methods=['get'])
    def spans(self, request, pk=None):
        """Get all spans for a trace."""
        trace = self.get_object()
        serializer = SpanSerializer(trace.spans.all(), many=True)
        return Response(serializer.data)


class SpanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Span model.
    Provides CRUD operations for spans.
    """
    queryset = Span.objects.all()
    serializer_class = SpanSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['trace', 'status']
    ordering = ['start_time']
