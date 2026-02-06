from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import ServiceRegistry, DependencyMap, DeploymentEvent, ConfigWatcher, KubernetesPod, KubernetesDeployment
from .serializers import (
    ServiceRegistrySerializer, DependencyMapSerializer, 
    DeploymentEventSerializer, ConfigWatcherSerializer,
    KubernetesPodSerializer, KubernetesDeploymentSerializer
)

class ServiceRegistryViewSet(viewsets.ModelViewSet):
    queryset = ServiceRegistry.objects.filter(is_active=True)
    serializer_class = ServiceRegistrySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['language', 'framework', 'owner_team']
    search_fields = ['name']

class DependencyMapViewSet(viewsets.ModelViewSet):
    queryset = DependencyMap.objects.all()
    serializer_class = DependencyMapSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['dependency_type', 'is_critical']
    search_fields = ['consumer__name', 'provider__name']

class DeploymentEventViewSet(viewsets.ModelViewSet):
    queryset = DeploymentEvent.objects.filter(is_active=True)
    serializer_class = DeploymentEventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'environment']
    search_fields = ['service__name', 'version', 'commit_hash']

class ConfigWatcherViewSet(viewsets.ModelViewSet):
    queryset = ConfigWatcher.objects.all()
    serializer_class = ConfigWatcherSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['source_type', 'change_type']
    search_fields = ['key', 'source_name']

class KubernetesPodViewSet(viewsets.ModelViewSet):
    queryset = KubernetesPod.objects.filter(is_active=True)
    serializer_class = KubernetesPodSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['namespace', 'node_name', 'status']
    search_fields = ['pod_name', 'ip_address']

class KubernetesDeploymentViewSet(viewsets.ModelViewSet):
    queryset = KubernetesDeployment.objects.filter(is_active=True)
    serializer_class = KubernetesDeploymentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['namespace']
    search_fields = ['name']
