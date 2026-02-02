"""Application Metrics views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Sum
from .models import ApplicationMetric, EndpointMetric
from .serializers import ApplicationMetricSerializer, EndpointMetricSerializer


class ApplicationMetricViewSet(viewsets.ModelViewSet):
    queryset = ApplicationMetric.objects.filter(is_active=True)
    serializer_class = ApplicationMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['app_name', 'environment', 'source']
    search_fields = ['app_name']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary of application metrics."""
        qs = self.get_queryset()
        summary = qs.aggregate(
            total_requests=Sum('request_count'),
            total_errors=Sum('error_count'),
            avg_latency=Avg('avg_latency_ms')
        )
        return Response(summary)

    @action(detail=False, methods=['get'])
    def by_app(self, request):
        """Get metrics grouped by app."""
        app_name = request.query_params.get('app_name')
        if not app_name:
            return Response({'error': 'app_name required'}, status=400)
        metrics = self.get_queryset().filter(app_name=app_name)[:100]
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)


class EndpointMetricViewSet(viewsets.ModelViewSet):
    queryset = EndpointMetric.objects.filter(is_active=True)
    serializer_class = EndpointMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['app_name', 'endpoint', 'method']
    search_fields = ['endpoint']
    ordering = ['-timestamp']
