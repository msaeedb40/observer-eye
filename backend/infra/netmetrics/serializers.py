"""Network Metrics serializers."""
from rest_framework import serializers
from .models import NetworkMetric, ConnectionMetric


class NetworkMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ConnectionMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
