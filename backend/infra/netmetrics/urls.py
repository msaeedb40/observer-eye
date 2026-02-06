"""Network Metrics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'netmetrics'

router = DefaultRouter()
router.register(r'network', views.NetworkMetricViewSet, basename='network-metric')
router.register(r'connections', views.ConnectionMetricViewSet, basename='connection-metric')
router.register(r'service-mesh', views.ServiceMeshMetricViewSet, basename='service-mesh-metric')
router.register(r'dns', views.DNSMetricViewSet, basename='dns-metric')
router.register(r'certificates', views.TLSCertificateViewSet, basename='tls-certificate')
router.register(r'dependencies', views.ServiceDependencyViewSet, basename='service-dependency')

urlpatterns = [
    path('', include(router.urls)),
]
