from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemResourceViewSet, 
    KubernetesClusterViewSet, 
    KubernetesNodeViewSet, 
    KubernetesPodViewSet, 
    CloudResourceViewSet
)

app_name = 'system'

router = DefaultRouter()
router.register(r'resources', SystemResourceViewSet)
router.register(r'clusters', KubernetesClusterViewSet)
router.register(r'nodes', KubernetesNodeViewSet)
router.register(r'pods', KubernetesPodViewSet)
router.register(r'cloud-resources', CloudResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
