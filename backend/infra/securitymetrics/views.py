"""Security Metrics views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import SecurityMetric, ThreatEvent, AuditLog
from .serializers import SecurityMetricSerializer, ThreatEventSerializer, AuditLogSerializer


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
