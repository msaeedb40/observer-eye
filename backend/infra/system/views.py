from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import SystemResource, KubernetesCluster, KubernetesNode, KubernetesPod, CloudResource
from .serializers import (
    SystemResourceSerializer, KubernetesClusterSerializer, 
    KubernetesNodeSerializer, KubernetesPodSerializer, CloudResourceSerializer
)

class SystemResourceViewSet(viewsets.ModelViewSet):
    queryset = SystemResource.objects.filter(is_active=True)
    serializer_class = SystemResourceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'environment', 'region']
    search_fields = ['hostname', 'os_name']

class KubernetesClusterViewSet(viewsets.ModelViewSet):
    queryset = KubernetesCluster.objects.filter(is_active=True)
    serializer_class = KubernetesClusterSerializer
    permission_classes = [AllowAny]

class KubernetesNodeViewSet(viewsets.ModelViewSet):
    queryset = KubernetesNode.objects.filter(is_active=True)
    serializer_class = KubernetesNodeSerializer
    permission_classes = [AllowAny]

class KubernetesPodViewSet(viewsets.ModelViewSet):
    queryset = KubernetesPod.objects.filter(is_active=True)
    serializer_class = KubernetesPodSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cluster', 'node', 'phase', 'namespace']
    search_fields = ['name', 'namespace']

class CloudResourceViewSet(viewsets.ModelViewSet):
    queryset = CloudResource.objects.filter(is_active=True)
    serializer_class = CloudResourceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['provider', 'resource_type', 'region']
    search_fields = ['name', 'resource_id']
