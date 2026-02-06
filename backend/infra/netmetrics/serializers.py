"""Network Metrics serializers."""
from rest_framework import serializers
from .models import NetworkMetric, ConnectionMetric
from .service_mesh import ServiceMeshMetric, DNSMetric, TLSCertificate, ServiceDependency


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


class ServiceMeshMetricSerializer(serializers.ModelSerializer):
    success_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = ServiceMeshMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class DNSMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class TLSCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLSCertificate
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ServiceDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDependency
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'discovered_at', 'last_seen']
