"""Security Metrics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'securitymetrics'

router = DefaultRouter()
router.register(r'security', views.SecurityMetricViewSet, basename='security-metric')
router.register(r'threats', views.ThreatEventViewSet, basename='threat-event')
router.register(r'audit', views.AuditLogViewSet, basename='audit-log')
router.register(r'vulnerabilities', views.VulnerabilityScanViewSet, basename='vulnerability-scan')
router.register(r'compliance/frameworks', views.ComplianceFrameworkViewSet, basename='compliance-framework')
router.register(r'compliance/checks', views.ComplianceCheckViewSet, basename='compliance-check')
router.register(r'incidents', views.SecurityIncidentViewSet, basename='security-incident')
router.register(r'policies', views.SecurityPolicyViewSet, basename='security-policy')

urlpatterns = [
    path('', include(router.urls)),
]
