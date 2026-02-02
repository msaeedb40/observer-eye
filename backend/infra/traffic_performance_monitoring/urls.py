"""Traffic Performance Monitoring URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import TrafficPerformanceViewSet

app_name = 'traffic_performance_monitoring'

router = DefaultRouter()
router.register(r'performance', TrafficPerformanceViewSet, basename='traffic-performance')

urlpatterns = [path('', include(router.urls))]
