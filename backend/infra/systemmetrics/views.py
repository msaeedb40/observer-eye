"""System Metrics views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from .models import SystemMetric, DiskMetric, ProcessMetric
from .serializers import SystemMetricSerializer, DiskMetricSerializer, ProcessMetricSerializer


class SystemMetricViewSet(viewsets.ModelViewSet):
    queryset = SystemMetric.objects.filter(is_active=True)
    serializer_class = SystemMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'source']
    search_fields = ['host', 'hostname']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest metrics per host."""
        hosts = self.get_queryset().values_list('host', flat=True).distinct()
        result = []
        for host in hosts[:50]:
            latest = self.get_queryset().filter(host=host).first()
            if latest:
                result.append(self.get_serializer(latest).data)
        return Response(result)


class DiskMetricViewSet(viewsets.ModelViewSet):
    queryset = DiskMetric.objects.filter(is_active=True)
    serializer_class = DiskMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['host', 'mount_point']
    ordering = ['-timestamp']


class ProcessMetricViewSet(viewsets.ModelViewSet):
    queryset = ProcessMetric.objects.filter(is_active=True)
    serializer_class = ProcessMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'name', 'status']
    search_fields = ['name']
    ordering = ['-cpu_percent']
