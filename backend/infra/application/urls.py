from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceRegistryViewSet, 
    DependencyMapViewSet, 
    DeploymentEventViewSet, 
    ConfigWatcherViewSet,
    KubernetesPodViewSet,
    KubernetesDeploymentViewSet
)

app_name = 'application'

router = DefaultRouter()
router.register(r'registry', ServiceRegistryViewSet)
router.register(r'dependency-map', DependencyMapViewSet)
router.register(r'deployments', DeploymentEventViewSet)
router.register(r'config-watcher', ConfigWatcherViewSet)
router.register(r'k8s-pods', KubernetesPodViewSet)
router.register(r'k8s-deployments', KubernetesDeploymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
