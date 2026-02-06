from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkInterface, TrafficFlow, FirewallRule, VPNConnection
from .serializers import NetworkInterfaceSerializer, TrafficFlowSerializer, FirewallRuleSerializer, VPNConnectionSerializer

class NetworkInterfaceViewSet(viewsets.ModelViewSet):
    queryset = NetworkInterface.objects.filter(is_active=True)
    serializer_class = NetworkInterfaceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'hostname']
    search_fields = ['interface_name', 'ipv4_address']

class TrafficFlowViewSet(viewsets.ModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['protocol', 'source_ip', 'destination_ip']
    search_fields = ['source_ip', 'destination_ip']

class FirewallRuleViewSet(viewsets.ModelViewSet):
    queryset = FirewallRule.objects.filter(is_active=True)
    serializer_class = FirewallRuleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['action', 'is_active']
    search_fields = ['name', 'source_cidr']

class VPNConnectionViewSet(viewsets.ModelViewSet):
    queryset = VPNConnection.objects.filter(is_active=True)
    serializer_class = VPNConnectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'tunnel_status']
    search_fields = ['connection_id', 'remote_gateway']
