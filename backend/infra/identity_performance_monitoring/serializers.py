"""Identity Performance Monitoring serializers, views, URLs."""
from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import IdentityPerformance


class IdentityPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityPerformance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class IdentityPerformanceViewSet(viewsets.ModelViewSet):
    queryset = IdentityPerformance.objects.filter(is_active=True)
    serializer_class = IdentityPerformanceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['auth_type', 'provider', 'success']
    ordering = ['-timestamp']
