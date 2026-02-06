from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import LogPipeline, SanitizationRule
from .serializers import LogPipelineSerializer, SanitizationRuleSerializer


class LogPipelineViewSet(viewsets.ModelViewSet):
    queryset = LogPipeline.objects.filter(is_active=True)
    serializer_class = LogPipelineSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['source_type', 'enabled']
    search_fields = ['name', 'description']


class SanitizationRuleViewSet(viewsets.ModelViewSet):
    queryset = SanitizationRule.objects.filter(is_active=True)
    serializer_class = SanitizationRuleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['pattern_type', 'enabled', 'is_global']
    search_fields = ['name', 'pattern']
