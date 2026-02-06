from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import ThreatEvent, AuditTrail, VulnerabilityScan, CompliancePolicy
from .serializers import ThreatEventSerializer, AuditTrailSerializer, VulnerabilityScanSerializer, CompliancePolicySerializer

class ThreatEventViewSet(viewsets.ModelViewSet):
    queryset = ThreatEvent.objects.filter(is_active=True)
    serializer_class = ThreatEventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['severity', 'status', 'threat_type']
    search_fields = ['description', 'source_ip']

class AuditTrailViewSet(viewsets.ModelViewSet):
    queryset = AuditTrail.objects.all()
    serializer_class = AuditTrailSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['action', 'actor']
    search_fields = ['target', 'changes']

class VulnerabilityScanViewSet(viewsets.ModelViewSet):
    queryset = VulnerabilityScan.objects.filter(is_active=True)
    serializer_class = VulnerabilityScanSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['severity', 'status', 'scan_tpe']
    search_fields = ['target', 'cve_id']

class CompliancePolicyViewSet(viewsets.ModelViewSet):
    queryset = CompliancePolicy.objects.filter(is_active=True)
    serializer_class = CompliancePolicySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['framework', 'last_check_status']
    search_fields = ['name']
