"""Security Metrics serializers."""
from rest_framework import serializers
from .models import SecurityMetric, ThreatEvent, AuditLog


class SecurityMetricSerializer(serializers.ModelSerializer):
    auth_failure_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = SecurityMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ThreatEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatEvent
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'timestamp']
