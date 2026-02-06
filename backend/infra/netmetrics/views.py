"""Network Metrics views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import NetworkMetric, ConnectionMetric
from .service_mesh import ServiceMeshMetric, DNSMetric, TLSCertificate, ServiceDependency
from .serializers import (
    NetworkMetricSerializer, ConnectionMetricSerializer,
    ServiceMeshMetricSerializer, DNSMetricSerializer,
    TLSCertificateSerializer, ServiceDependencySerializer
)


class NetworkMetricViewSet(viewsets.ModelViewSet):
    queryset = NetworkMetric.objects.filter(is_active=True)
    serializer_class = NetworkMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'interface', 'source']
    search_fields = ['host', 'interface']
    ordering = ['-timestamp']


class ConnectionMetricViewSet(viewsets.ModelViewSet):
    queryset = ConnectionMetric.objects.filter(is_active=True)
    serializer_class = ConnectionMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'source']
    search_fields = ['host']
    ordering = ['-timestamp']


class ServiceMeshMetricViewSet(viewsets.ModelViewSet):
    """Service mesh metrics viewset."""
    queryset = ServiceMeshMetric.objects.filter(is_active=True)
    serializer_class = ServiceMeshMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source_service', 'destination_service', 'source_namespace', 'destination_namespace', 'protocol']
    search_fields = ['source_service', 'destination_service']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def topology(self, request):
        """Get service topology data for graph visualization."""
        qs = self.get_queryset().values(
            'source_service', 'destination_service'
        ).annotate(
            request_count=Count('id'),
            avg_latency=Avg('latency_p50_ms')
        )
        return Response(list(qs))

    @action(detail=False, methods=['get'])
    def errors(self, request):
        """Get services with high error rates."""
        qs = self.get_queryset().filter(error_count__gt=0).order_by('-error_count')
        return Response(self.get_serializer(qs[:50], many=True).data)


class DNSMetricViewSet(viewsets.ModelViewSet):
    """DNS metrics viewset."""
    queryset = DNSMetric.objects.filter(is_active=True)
    serializer_class = DNSMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'query_domain', 'query_type', 'status']
    search_fields = ['query_domain']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def slow(self, request):
        """Get slow DNS queries (>100ms)."""
        qs = self.get_queryset().filter(response_time_ms__gt=100)
        return Response(self.get_serializer(qs[:50], many=True).data)


class TLSCertificateViewSet(viewsets.ModelViewSet):
    """TLS certificate viewset."""
    queryset = TLSCertificate.objects.all()
    serializer_class = TLSCertificateSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'domain', 'is_valid']
    search_fields = ['domain', 'issuer']
    ordering = ['days_until_expiry']

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get certificates expiring within 30 days."""
        qs = self.get_queryset().filter(days_until_expiry__lte=30, is_valid=True)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    def invalid(self, request):
        """Get invalid certificates."""
        qs = self.get_queryset().filter(is_valid=False)
        return Response(self.get_serializer(qs, many=True).data)


class ServiceDependencyViewSet(viewsets.ModelViewSet):
    """Service dependency viewset."""
    queryset = ServiceDependency.objects.filter(is_active=True)
    serializer_class = ServiceDependencySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['source_service', 'target_service', 'dependency_type']
    search_fields = ['source_service', 'target_service']

    @action(detail=False, methods=['get'])
    def graph(self, request):
        """Get dependency graph data."""
        qs = self.get_queryset().values(
            'source_service', 'source_namespace',
            'target_service', 'target_namespace',
            'dependency_type', 'avg_latency_ms', 'error_rate'
        )
        return Response(list(qs))
