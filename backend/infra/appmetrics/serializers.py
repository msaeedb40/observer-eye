"""Application Metrics serializers."""
from rest_framework import serializers
from .models import ApplicationMetric, EndpointMetric


class ApplicationMetricSerializer(serializers.ModelSerializer):
    error_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = ApplicationMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class EndpointMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndpointMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
