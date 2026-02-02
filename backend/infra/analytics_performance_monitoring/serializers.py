"""Analytics Performance Monitoring serializers, views, URLs, admin."""
from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import AnalyticsPerformance


class AnalyticsPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsPerformance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AnalyticsPerformanceViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsPerformance.objects.filter(is_active=True)
    serializer_class = AnalyticsPerformanceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['query_type', 'cache_hit']
    ordering = ['-timestamp']
