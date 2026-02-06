from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import CloudMetric, CloudCost
from .serializers import CloudMetricSerializer, CloudCostSerializer

class CloudMetricViewSet(viewsets.ModelViewSet):
    queryset = CloudMetric.objects.filter(is_active=True)
    serializer_class = CloudMetricSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['resource_type', 'metric_name']
    search_fields = ['resource_id']

class CloudCostViewSet(viewsets.ModelViewSet):
    queryset = CloudCost.objects.filter(is_active=True)
    serializer_class = CloudCostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['usage_type', 'currency']
    search_fields = ['resource_id']
