"""Traffic and RUM URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'traffic'

router = DefaultRouter()
router.register(r'stats', views.TrafficStatsViewSet, basename='traffic-stats')
router.register(r'route-analytics', views.RouteAnalyticsViewSet, basename='route-analytics')
router.register(r'lb-stats', views.LoadBalancerStatsViewSet, basename='lb-stats')

# RUM endpoints
router.register(r'rum/sessions', views.UserSessionViewSet, basename='user-session')
router.register(r'rum/page-views', views.PageViewViewSet, basename='page-view')
router.register(r'rum/vitals', views.CoreWebVitalsViewSet, basename='core-web-vitals')
router.register(r'rum/errors', views.FrontendErrorViewSet, basename='frontend-error')
router.register(r'rum/resources', views.ResourceTimingViewSet, basename='resource-timing')

# Synthetic Monitoring endpoints
router.register(r'synthetic/monitors', views.SyntheticMonitorViewSet, basename='synthetic-monitor')
router.register(r'synthetic/results', views.SyntheticResultViewSet, basename='synthetic-result')

urlpatterns = [
    path('', include(router.urls)),
]
