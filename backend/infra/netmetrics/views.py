"""Network Metrics views."""
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkMetric, ConnectionMetric
from .serializers import NetworkMetricSerializer, ConnectionMetricSerializer


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
