"""
URL configuration for Observer-Eye Backend Infrastructure.

Observer-Eye Observability Platform - Data Layer API Routes
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """Health check endpoint for observability."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'observer-eye-backend',
        'version': '1.0.0'
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # API v1 Routes
    path('api/v1/', include([
        # Core
        path('core/', include('core.urls', namespace='core')),
        
        # Metrics
        path('appmetrics/', include('appmetrics.urls', namespace='appmetrics')),
        path('netmetrics/', include('netmetrics.urls', namespace='netmetrics')),
        path('systemmetrics/', include('systemmetrics.urls', namespace='systemmetrics')),
        path('securitymetrics/', include('securitymetrics.urls', namespace='securitymetrics')),
        
        # Performance Monitoring
        path('analytics-perf/', include('analytics_performance_monitoring.urls', namespace='analytics_perf')),
        path('apm/', include('application_performance_monitoring.urls', namespace='apm')),
        path('identity-perf/', include('identity_performance_monitoring.urls', namespace='identity_perf')),
        path('security-perf/', include('security_performance_monitoring.urls', namespace='security_perf')),
        path('system-perf/', include('system_performance_monitoring.urls', namespace='system_perf')),
        path('traffic-perf/', include('traffic_performance_monitoring.urls', namespace='traffic_perf')),
        
        # Analytics & Insights
        path('analytics/', include('analytics.urls', namespace='analytics')),
        path('insights/', include('insights_observer.urls', namespace='insights')),
        
        # Platform Services
        path('integration/', include('integration.urls', namespace='integration')),
        path('notification/', include('notification.urls', namespace='notification')),
        path('queriers/', include('queriers.urls', namespace='queriers')),
        path('settings/', include('settings.urls', namespace='settings')),
        path('dashboards/', include('template_dashboards.urls', namespace='dashboards')),
        path('grailobserver/', include('grailobserver.urls', namespace='grailobserver')),
    ])),
]
