from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThreatEventViewSet, AuditTrailViewSet, VulnerabilityScanViewSet, CompliancePolicyViewSet

app_name = 'security'

router = DefaultRouter()
router.register(r'threats', ThreatEventViewSet)
router.register(r'audit', AuditTrailViewSet)
router.register(r'vulnerability-scans', VulnerabilityScanViewSet)
router.register(r'compliance-policies', CompliancePolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
