"""Application Metrics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'appmetrics'

router = DefaultRouter()
router.register(r'applications', views.ApplicationMetricViewSet, basename='application-metric')
router.register(r'endpoints', views.EndpointMetricViewSet, basename='endpoint-metric')

urlpatterns = [
    path('', include(router.urls)),
]
