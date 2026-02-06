"""Template Dashboards views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import DashboardTemplate, TemplateInstance, FeaturedTemplate, VariableCatalog
from .serializers import (
    DashboardTemplateSerializer, 
    DashboardTemplateListSerializer, 
    TemplateInstanceSerializer,
    FeaturedTemplateSerializer,
    VariableCatalogSerializer
)


class DashboardTemplateViewSet(viewsets.ModelViewSet):
    queryset = DashboardTemplate.objects.filter(is_active=True)
    serializer_class = DashboardTemplateSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_official']
    search_fields = ['name', 'description']
    ordering = ['-downloads', '-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return DashboardTemplateListSerializer
        return DashboardTemplateSerializer

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """Apply template to create a new instance."""
        template = self.get_object()
        template.downloads += 1
        template.save()
        
        instance = TemplateInstance.objects.create(
            template=template,
            user_id=request.data.get('user_id', 'anonymous'),
            name=request.data.get('name', template.name),
            variable_values=request.data.get('variables', {})
        )
        return Response(TemplateInstanceSerializer(instance).data)


class TemplateInstanceViewSet(viewsets.ModelViewSet):
    queryset = TemplateInstance.objects.filter(is_active=True)
    serializer_class = TemplateInstanceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user_id', 'template']
    search_fields = ['name']

class FeaturedTemplateViewSet(viewsets.ModelViewSet):
    queryset = FeaturedTemplate.objects.all()
    serializer_class = FeaturedTemplateSerializer
    permission_classes = [AllowAny]
    ordering = ['order']

class VariableCatalogViewSet(viewsets.ModelViewSet):
    queryset = VariableCatalog.objects.filter(is_active=True)
    serializer_class = VariableCatalogSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['variable_type', 'is_global']
    search_fields = ['name', 'description']
