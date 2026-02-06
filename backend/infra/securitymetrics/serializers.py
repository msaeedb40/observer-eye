from rest_framework import serializers
from .models import SecurityMetric, ThreatEvent, AuditLog
from .vulnerability import (
    VulnerabilityScan, ComplianceFramework, ComplianceCheck,
    SecurityIncident, SecurityPolicy
)


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
        read_only_fields = ['id', 'created_at']


class VulnerabilityScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = VulnerabilityScan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'first_detected', 'last_seen']


class ComplianceFrameworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceFramework
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ComplianceCheckSerializer(serializers.ModelSerializer):
    framework_name = serializers.CharField(source='framework.name', read_only=True)

    class Meta:
        model = ComplianceCheck
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SecurityIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityIncident
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SecurityPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPolicy
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
