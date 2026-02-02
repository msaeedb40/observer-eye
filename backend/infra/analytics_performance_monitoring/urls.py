"""Analytics Performance Monitoring URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import AnalyticsPerformanceViewSet

app_name = 'analytics_performance_monitoring'

router = DefaultRouter()
router.register(r'performance', AnalyticsPerformanceViewSet, basename='analytics-performance')

urlpatterns = [path('', include(router.urls))]
