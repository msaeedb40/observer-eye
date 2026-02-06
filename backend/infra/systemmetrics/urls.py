"""System Metrics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'systemmetrics'

router = DefaultRouter()
router.register(r'system', views.SystemMetricViewSet, basename='system-metric')
router.register(r'disk', views.DiskMetricViewSet, basename='disk-metric')
router.register(r'process', views.ProcessMetricViewSet, basename='process-metric')
router.register(r'container', views.ContainerMetricViewSet, basename='container-metric')
router.register(r'kubernetes/events', views.KubernetesEventViewSet, basename='kubernetes-event')
router.register(r'kubernetes/pods', views.KubernetesPodViewSet, basename='kubernetes-pod')
router.register(r'gpu', views.GPUMetricViewSet, basename='gpu-metric')

urlpatterns = [
    path('', include(router.urls)),
]
