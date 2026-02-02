"""Insights Observer views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Insight, AnomalyDetection
from .serializers import InsightSerializer, AnomalyDetectionSerializer


class InsightViewSet(viewsets.ModelViewSet):
    queryset = Insight.objects.filter(is_active=True)
    serializer_class = InsightSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['insight_type', 'severity', 'status']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an insight."""
        insight = self.get_object()
        insight.status = 'acknowledged'
        insight.save()
        return Response({'status': 'acknowledged'})

    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Dismiss an insight."""
        insight = self.get_object()
        insight.status = 'dismissed'
        insight.save()
        return Response({'status': 'dismissed'})


class AnomalyDetectionViewSet(viewsets.ModelViewSet):
    queryset = AnomalyDetection.objects.filter(is_active=True)
    serializer_class = AnomalyDetectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['metric_name', 'source', 'is_resolved']
    search_fields = ['metric_name', 'source']
    ordering = ['-detected_at']
