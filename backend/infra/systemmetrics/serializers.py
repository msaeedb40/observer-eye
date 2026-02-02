"""System Metrics serializers."""
from rest_framework import serializers
from .models import SystemMetric, DiskMetric, ProcessMetric


class SystemMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class DiskMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ProcessMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
