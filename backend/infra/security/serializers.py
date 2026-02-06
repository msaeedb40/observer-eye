from rest_framework import serializers
from .models import ThreatEvent, AuditTrail, VulnerabilityScan, CompliancePolicy

class ThreatEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatEvent
        fields = '__all__'

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'

class VulnerabilityScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = VulnerabilityScan
        fields = '__all__'

class CompliancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompliancePolicy
        fields = '__all__'
