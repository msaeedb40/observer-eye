"""Security Metrics views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import SecurityMetric, ThreatEvent, AuditLog
from .vulnerability import (
    VulnerabilityScan, ComplianceFramework, ComplianceCheck,
    SecurityIncident, SecurityPolicy
)
from .serializers import (
    SecurityMetricSerializer, ThreatEventSerializer, AuditLogSerializer,
    VulnerabilityScanSerializer, ComplianceFrameworkSerializer,
    ComplianceCheckSerializer, SecurityIncidentSerializer, SecurityPolicySerializer
)


class SecurityMetricViewSet(viewsets.ModelViewSet):
    queryset = SecurityMetric.objects.filter(is_active=True)
    serializer_class = SecurityMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'source']
    search_fields = ['host']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get security summary."""
        qs = self.get_queryset()
        from django.db.models import Sum
        summary = qs.aggregate(
            total_auth_attempts=Sum('auth_attempts'),
            total_auth_failures=Sum('auth_failures'),
            total_blocked=Sum('blocked_requests')
        )
        return Response(summary)


class ThreatEventViewSet(viewsets.ModelViewSet):
    queryset = ThreatEvent.objects.filter(is_active=True)
    serializer_class = ThreatEventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'threat_type', 'severity', 'blocked']
    search_fields = ['description', 'threat_type']
    ordering = ['-timestamp']


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'action', 'resource', 'success']
    search_fields = ['user', 'action', 'resource']
    ordering = ['-timestamp']
    http_method_names = ['get', 'post', 'head']  # Audit logs should not be updated/deleted


class VulnerabilityScanViewSet(viewsets.ModelViewSet):
    """Vulnerability scanning results viewset."""
    queryset = VulnerabilityScan.objects.all()
    serializer_class = VulnerabilityScanSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['host', 'scan_type', 'severity', 'remediation_status', 'cve_id']
    search_fields = ['cve_id', 'package_name']
    ordering = ['-first_detected']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get vulnerability summary by severity."""
        qs = self.get_queryset().filter(remediation_status='open')
        summary = qs.values('severity').annotate(count=Count('id'))
        return Response({item['severity']: item['count'] for item in summary})

    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Get critical and high vulnerabilities."""
        qs = self.get_queryset().filter(
            severity__in=['critical', 'high'],
            remediation_status='open'
        )
        return Response(self.get_serializer(qs[:100], many=True).data)


class ComplianceFrameworkViewSet(viewsets.ModelViewSet):
    """Compliance framework viewset."""
    queryset = ComplianceFramework.objects.filter(is_active=True)
    serializer_class = ComplianceFrameworkSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ComplianceCheckViewSet(viewsets.ModelViewSet):
    """Compliance check results viewset."""
    queryset = ComplianceCheck.objects.all()
    serializer_class = ComplianceCheckSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['framework', 'status', 'category']
    search_fields = ['control_id', 'control_name']
    ordering = ['-last_checked']

    @action(detail=False, methods=['get'])
    def failing(self, request):
        """Get all failing compliance checks."""
        qs = self.get_queryset().filter(status='fail')
        return Response(self.get_serializer(qs, many=True).data)


class SecurityIncidentViewSet(viewsets.ModelViewSet):
    """Security incident viewset."""
    queryset = SecurityIncident.objects.all()
    serializer_class = SecurityIncidentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['severity', 'status', 'category', 'assignee']
    search_fields = ['title', 'description', 'incident_id']
    ordering = ['-detected_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active incidents."""
        qs = self.get_queryset().exclude(status__in=['resolved', 'closed'])
        return Response(self.get_serializer(qs, many=True).data)


class SecurityPolicyViewSet(viewsets.ModelViewSet):
    """Security policy viewset."""
    queryset = SecurityPolicy.objects.all()
    serializer_class = SecurityPolicySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_enabled', 'enforcement_mode']
    search_fields = ['name', 'description']
