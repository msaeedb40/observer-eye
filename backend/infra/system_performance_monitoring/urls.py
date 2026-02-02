"""System Performance Monitoring URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import SystemPerformanceViewSet

app_name = 'system_performance_monitoring'

router = DefaultRouter()
router.register(r'performance', SystemPerformanceViewSet, basename='system-performance')

urlpatterns = [path('', include(router.urls))]
