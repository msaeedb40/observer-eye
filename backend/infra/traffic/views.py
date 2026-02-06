from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Sum
from .models import TrafficStats, RouteAnalytics, LoadBalancerStats
from .rum import CoreWebVitals, UserSession, PageView, FrontendError, ResourceTiming
from .synthetic import SyntheticMonitor, SyntheticResult
from .serializers import (
    TrafficStatsSerializer, RouteAnalyticsSerializer, LoadBalancerStatsSerializer,
    CoreWebVitalsSerializer, UserSessionSerializer, PageViewSerializer,
    FrontendErrorSerializer, ResourceTimingSerializer,
    SyntheticMonitorSerializer, SyntheticResultSerializer
)


class TrafficStatsViewSet(viewsets.ModelViewSet):
    queryset = TrafficStats.objects.all()
    serializer_class = TrafficStatsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['timestamp', 'total_requests']
    ordering = ['-timestamp']


class RouteAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = RouteAnalytics.objects.all()
    serializer_class = RouteAnalyticsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['method', 'service']
    search_fields = ['route_path']


class LoadBalancerStatsViewSet(viewsets.ModelViewSet):
    queryset = LoadBalancerStats.objects.all()
    serializer_class = LoadBalancerStatsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['lb_name']


class UserSessionViewSet(viewsets.ModelViewSet):
    """User sessions viewset."""
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user_id', 'device_type', 'browser', 'country_code']
    ordering = ['-started_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get currently active sessions."""
        qs = self.get_queryset().filter(ended_at__isnull=True)
        return Response(self.get_serializer(qs[:100], many=True).data)


class PageViewViewSet(viewsets.ModelViewSet):
    """Page views viewset."""
    queryset = PageView.objects.all()
    serializer_class = PageViewSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['page_path', 'session']
    search_fields = ['page_path', 'page_title']

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most visited pages."""
        qs = self.get_queryset().values('page_path').annotate(
            views=Count('id')
        ).order_by('-views')
        return Response(list(qs[:20]))


class CoreWebVitalsViewSet(viewsets.ModelViewSet):
    """Core Web Vitals viewset."""
    queryset = CoreWebVitals.objects.all()
    serializer_class = CoreWebVitalsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['page_path', 'device_type', 'browser']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Aggregate Core Web Vitals across pages."""
        qs = self.get_queryset().aggregate(
            avg_lcp=Avg('lcp_ms'),
            avg_fid=Avg('fid_ms'),
            avg_cls=Avg('cls'),
            avg_ttfb=Avg('ttfb_ms')
        )
        return Response(qs)


class FrontendErrorViewSet(viewsets.ModelViewSet):
    """Frontend errors viewset."""
    queryset = FrontendError.objects.all()
    serializer_class = FrontendErrorSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['error_type', 'browser', 'os']
    search_fields = ['error_message', 'filename']
    ordering = ['-last_seen']


class ResourceTimingViewSet(viewsets.ModelViewSet):
    """Resource timing viewset."""
    queryset = ResourceTiming.objects.all()
    serializer_class = ResourceTimingSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['resource_type', 'response_status']
    ordering = ['-duration_ms']


class SyntheticMonitorViewSet(viewsets.ModelViewSet):
    """Synthetic monitor configuration viewset."""
    queryset = SyntheticMonitor.objects.all()
    serializer_class = SyntheticMonitorSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['check_type', 'is_active', 'method']
    search_fields = ['name', 'url']


class SyntheticResultViewSet(viewsets.ModelViewSet):
    """Synthetic check results viewset."""
    queryset = SyntheticResult.objects.all()
    serializer_class = SyntheticResultSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['monitor', 'status', 'location']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def uptime(self, request):
        """Get uptime percentage per monitor."""
        from django.db.models import Count, Q
        qs = self.get_queryset().values('monitor__name').annotate(
            total=Count('id'),
            success=Count('id', filter=Q(status='success'))
        )
        results = [
            {
                'monitor': item['monitor__name'],
                'uptime': (item['success'] / item['total'] * 100) if item['total'] > 0 else 0
            }
            for item in qs
        ]
        return Response(results)
