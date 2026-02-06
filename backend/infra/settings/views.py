"""Settings views."""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Setting, UserPreference, FeatureFlag, WorkspaceSettings
from .serializers import (
    SettingSerializer, 
    UserPreferenceSerializer, 
    FeatureFlagSerializer,
    WorkspaceSettingsSerializer
)


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.filter(is_active=True)
    serializer_class = SettingSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_sensitive']
    search_fields = ['key', 'description']

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get settings organized by category."""
        categories = self.get_queryset().values_list('category', flat=True).distinct()
        result = {}
        for category in categories:
            settings = self.get_queryset().filter(category=category)
            result[category] = self.get_serializer(settings, many=True).data
        return Response(result)


class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.filter(is_active=True)
    serializer_class = UserPreferenceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'key']


class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.filter(is_active=True)
    serializer_class = FeatureFlagSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['enabled']
    search_fields = ['name', 'description']

    def toggle(self, request, pk=None):
        """Toggle feature flag."""
        flag = self.get_object()
        flag.enabled = not flag.enabled
        flag.save()
        return Response({'enabled': flag.enabled})


class WorkspaceSettingsViewSet(viewsets.ModelViewSet):
    queryset = WorkspaceSettings.objects.filter(is_active=True)
    serializer_class = WorkspaceSettingsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
