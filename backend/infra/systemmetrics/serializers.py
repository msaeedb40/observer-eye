"""System Metrics serializers."""
from rest_framework import serializers
from .models import SystemMetric, DiskMetric, ProcessMetric
from .container_metrics import ContainerMetric, KubernetesEvent, KubernetesPod, GPUMetric


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


class ContainerMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class KubernetesEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesEvent
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class KubernetesPodSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesPod
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class GPUMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPUMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
