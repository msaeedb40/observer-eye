"""System Performance Monitoring serializers and views."""
from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import SystemPerformance


class SystemPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPerformance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SystemPerformanceViewSet(viewsets.ModelViewSet):
    queryset = SystemPerformance.objects.filter(is_active=True)
    serializer_class = SystemPerformanceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['host', 'operation_type']
    ordering = ['-timestamp']
