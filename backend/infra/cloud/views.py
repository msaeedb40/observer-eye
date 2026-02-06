from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import CloudProvider, CloudRegion
from .serializers import CloudProviderSerializer, CloudRegionSerializer

class CloudProviderViewSet(viewsets.ModelViewSet):
    queryset = CloudProvider.objects.filter(is_active=True)
    serializer_class = CloudProviderSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['provider_type']
    search_fields = ['name', 'account_id']

class CloudRegionViewSet(viewsets.ModelViewSet):
    queryset = CloudRegion.objects.filter(is_active=True)
    serializer_class = CloudRegionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name']
