from rest_framework import serializers
from .models import NetworkInterface, TrafficFlow, FirewallRule, VPNConnection

class NetworkInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkInterface
        fields = '__all__'

class TrafficFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFlow
        fields = '__all__'

class FirewallRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirewallRule
        fields = '__all__'

class VPNConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPNConnection
        fields = '__all__'
