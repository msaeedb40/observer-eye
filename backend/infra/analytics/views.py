"""Analytics views."""
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Dashboard, Widget, Report, SavedQuery
from .serializers import DashboardSerializer, DashboardListSerializer, WidgetSerializer, ReportSerializer, SavedQuerySerializer


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.filter(is_active=True).prefetch_related('widgets')
    serializer_class = DashboardSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_public']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return DashboardListSerializer
        return DashboardSerializer


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.filter(is_active=True)
    serializer_class = WidgetSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['dashboard', 'widget_type']
    ordering = ['created_at']


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.filter(is_active=True)
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


class SavedQueryViewSet(viewsets.ModelViewSet):
    queryset = SavedQuery.objects.filter(is_active=True)
    serializer_class = SavedQuerySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['data_source']
    search_fields = ['name']
    ordering = ['-created_at']
