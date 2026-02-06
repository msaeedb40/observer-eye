"""Insights Observer views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Insight, AnomalyDetection
from .serializers import InsightSerializer, AnomalyDetectionSerializer


class InsightViewSet(viewsets.ModelViewSet):
    queryset = Insight.objects.filter(is_active=True)
    serializer_class = InsightSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['insight_type', 'severity', 'status']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an insight."""
        insight = self.get_object()
        insight.status = 'acknowledged'
        insight.save()
        return Response({'status': 'acknowledged'})

    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Dismiss an insight."""
        insight = self.get_object()
        insight.status = 'dismissed'
        insight.save()
        return Response({'status': 'dismissed'})

    @action(detail=False, methods=['get'])
    def forecast(self, request):
        """Generate forecast for a metric."""
        metric = request.query_params.get('metric', 'cpu')
        
        # MOCK IMPLEMENTATION: Return predicted values
        return Response({
            'metric': metric,
            'forecast': [
                {'time': 'now+1h', 'value': 450, 'ci_lower': 400, 'ci_upper': 500},
                {'time': 'now+2h', 'value': 480, 'ci_lower': 420, 'ci_upper': 540},
                {'time': 'now+3h', 'value': 520, 'ci_lower': 450, 'ci_upper': 590},
                {'time': 'now+4h', 'value': 410, 'ci_lower': 380, 'ci_upper': 440},
            ]
        })

    @action(detail=False, methods=['post'])
    def analyze_root_cause(self, request):
        """Trigger AI root cause analysis."""
        incident_id = request.data.get('incident_id')
        
        # MOCK MOCK IMPLEMENTATION
        return Response({
            'incident_id': incident_id,
            'root_cause': 'Memory leak in payment-service caused cascading latency.',
            'confidence': 0.89,
            'evidence': ['OOMKilled events', 'High heap usage correlation']
        })


class AnomalyDetectionViewSet(viewsets.ModelViewSet):
    queryset = AnomalyDetection.objects.filter(is_active=True)
    serializer_class = AnomalyDetectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['metric_name', 'source', 'is_resolved']
    search_fields = ['metric_name', 'source']
    ordering = ['-detected_at']
