"""Identity Performance Monitoring URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .serializers import IdentityPerformanceViewSet

app_name = 'identity_performance_monitoring'

router = DefaultRouter()
router.register(r'performance', IdentityPerformanceViewSet, basename='identity-performance')

urlpatterns = [path('', include(router.urls))]
