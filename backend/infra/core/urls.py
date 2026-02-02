"""Core app URL configuration with REST Framework routers."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'core'

router = DefaultRouter()
router.register(r'metrics', views.MetricViewSet, basename='metric')
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'logs', views.LogEntryViewSet, basename='log')
router.register(r'traces', views.TraceViewSet, basename='trace')
router.register(r'spans', views.SpanViewSet, basename='span')

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('', include(router.urls)),
]
