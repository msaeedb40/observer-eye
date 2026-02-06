"""Notification views."""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import NotificationChannel, AlertRule, Alert, NotificationHistory
from .reliability import calculate_reliability_metrics
from .serializers import NotificationChannelSerializer, AlertRuleSerializer, AlertSerializer, NotificationHistorySerializer


class NotificationChannelViewSet(viewsets.ModelViewSet):
    queryset = NotificationChannel.objects.filter(is_active=True)
    serializer_class = NotificationChannelSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['channel_type', 'is_default']
    search_fields = ['name']


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.filter(is_active=True)
    serializer_class = AlertRuleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['severity', 'enabled', 'condition_type']
    search_fields = ['name', 'description']

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle alert rule enabled state."""
        rule = self.get_object()
        rule.enabled = not rule.enabled
        rule.save()
        return Response({'enabled': rule.enabled})

    @action(detail=True, methods=['post'])
    def trigger_test(self, request, pk=None):
        """Trigger a test alert for this rule."""
        rule = self.get_object()
        
        # Create a test alert instance
        alert = Alert.objects.create(
            rule=rule,
            name=f"[TEST] {rule.name}",
            severity=rule.severity,
            message=f"This is a test alert for rule '{rule.name}'. No action required.",
            state='firing',
            labels={'test': 'true'}
        )
        
        return Response({
            'status': 'triggered', 
            'alert_id': alert.id,
            'message': 'Test alert sent to configured channels.'
        })



class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.filter(is_active=True)
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state', 'severity', 'rule']
    search_fields = ['name', 'message']
    ordering = ['-started_at']

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert."""
        alert = self.get_object()
        alert.state = 'acknowledged'
        alert.acknowledged_by = request.data.get('user', 'unknown')
        alert.save()
        return Response({'status': 'acknowledged'})

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an alert."""
        alert = self.get_object()
        alert.state = 'resolved'
        alert.resolved_at = timezone.now()
        alert.save()
        return Response({'status': 'resolved'})

    @action(detail=False, methods=['get'])
    def reliability(self, request):
        """Get reliability metrics (MTTD, MTTR, MTTS)."""
        metrics = calculate_reliability_metrics()
        return Response(metrics)


class NotificationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationHistory.objects.all()
    serializer_class = NotificationHistorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['alert', 'channel', 'status']
    ordering = ['-created_at']
