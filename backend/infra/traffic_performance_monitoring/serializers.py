"""Traffic Performance Monitoring serializers and views."""
from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import TrafficPerformance


class TrafficPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficPerformance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class TrafficPerformanceViewSet(viewsets.ModelViewSet):
    queryset = TrafficPerformance.objects.filter(is_active=True)
    serializer_class = TrafficPerformanceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['host', 'source']
    ordering = ['-timestamp']
