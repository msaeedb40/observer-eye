"""System Metrics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'systemmetrics'

router = DefaultRouter()
router.register(r'system', views.SystemMetricViewSet, basename='system-metric')
router.register(r'disk', views.DiskMetricViewSet, basename='disk-metric')
router.register(r'process', views.ProcessMetricViewSet, basename='process-metric')

urlpatterns = [
    path('', include(router.urls)),
]
