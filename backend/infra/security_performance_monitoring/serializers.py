"""Security Performance Monitoring serializers and views."""
from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import SecurityPerformance


class SecurityPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPerformance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SecurityPerformanceViewSet(viewsets.ModelViewSet):
    queryset = SecurityPerformance.objects.filter(is_active=True)
    serializer_class = SecurityPerformanceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['operation_type', 'source']
    ordering = ['-timestamp']
