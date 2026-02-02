"""Security Performance Monitoring URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import SecurityPerformanceViewSet

app_name = 'security_performance_monitoring'

router = DefaultRouter()
router.register(r'performance', SecurityPerformanceViewSet, basename='security-performance')

urlpatterns = [path('', include(router.urls))]
