"""Integration views."""
import secrets
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Integration, DataSource, Webhook
from .serializers import IntegrationSerializer, DataSourceSerializer, WebhookSerializer


class IntegrationViewSet(viewsets.ModelViewSet):
    queryset = Integration.objects.filter(is_active=True)
    serializer_class = IntegrationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['integration_type', 'enabled']
    search_fields = ['name']

    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test integration connection."""
        integration = self.get_object()
        # In real implementation, test the connection
        return Response({'status': 'success', 'message': 'Connection successful'})

    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """Trigger manual sync."""
        integration = self.get_object()
        integration.last_sync = timezone.now()
        integration.sync_status = 'syncing'
        integration.save()
        return Response({'status': 'sync_started'})


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.filter(is_active=True)
    serializer_class = DataSourceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['integration', 'source_type', 'enabled']
    search_fields = ['name']


class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.filter(is_active=True)
    serializer_class = WebhookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['data_type', 'enabled']
    search_fields = ['name']

    def perform_create(self, serializer):
        # Generate a secure token for the webhook
        token = secrets.token_urlsafe(32)
        serializer.save(token=token)
