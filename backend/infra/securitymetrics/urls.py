"""Security Metrics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'securitymetrics'

router = DefaultRouter()
router.register(r'security', views.SecurityMetricViewSet, basename='security-metric')
router.register(r'threats', views.ThreatEventViewSet, basename='threat-event')
router.register(r'audit', views.AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
]
