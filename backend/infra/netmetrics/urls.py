"""Network Metrics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'netmetrics'

router = DefaultRouter()
router.register(r'network', views.NetworkMetricViewSet, basename='network-metric')
router.register(r'connections', views.ConnectionMetricViewSet, basename='connection-metric')

urlpatterns = [
    path('', include(router.urls)),
]
