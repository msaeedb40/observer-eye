"""System Metrics views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from .models import SystemMetric, DiskMetric, ProcessMetric
from .container_metrics import ContainerMetric, KubernetesEvent, KubernetesPod, GPUMetric
from .serializers import (
    SystemMetricSerializer, DiskMetricSerializer, ProcessMetricSerializer,
    ContainerMetricSerializer, KubernetesEventSerializer, KubernetesPodSerializer, GPUMetricSerializer
)


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


class ContainerMetricViewSet(viewsets.ModelViewSet):
    """Container-level metrics viewset."""
    queryset = ContainerMetric.objects.filter(is_active=True)
    serializer_class = ContainerMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'container_name', 'namespace', 'pod_name', 'status']
    search_fields = ['container_name', 'image', 'pod_name']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def by_namespace(self, request):
        """Get containers grouped by namespace."""
        namespace = request.query_params.get('namespace')
        if namespace:
            qs = self.get_queryset().filter(namespace=namespace)
        else:
            qs = self.get_queryset()
        return Response(self.get_serializer(qs[:100], many=True).data)


class KubernetesEventViewSet(viewsets.ModelViewSet):
    """Kubernetes events viewset."""
    queryset = KubernetesEvent.objects.all()
    serializer_class = KubernetesEventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cluster', 'namespace', 'kind', 'event_type', 'reason']
    search_fields = ['name', 'message', 'reason']
    ordering = ['-created_at']


class KubernetesPodViewSet(viewsets.ModelViewSet):
    """Kubernetes pods viewset."""
    queryset = KubernetesPod.objects.all()
    serializer_class = KubernetesPodSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cluster', 'namespace', 'phase', 'node_name']
    search_fields = ['name', 'node_name']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def by_node(self, request):
        """Get pods per node."""
        node = request.query_params.get('node')
        if node:
            qs = self.get_queryset().filter(node_name=node)
            return Response(self.get_serializer(qs, many=True).data)
        return Response({'error': 'node parameter required'}, status=400)


class GPUMetricViewSet(viewsets.ModelViewSet):
    """GPU metrics viewset."""
    queryset = GPUMetric.objects.filter(is_active=True)
    serializer_class = GPUMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['host', 'gpu_index', 'gpu_name']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def high_utilization(self, request):
        """Get GPUs with high utilization (>80%)."""
        qs = self.get_queryset().filter(utilization_percent__gte=80)
        return Response(self.get_serializer(qs[:50], many=True).data)
