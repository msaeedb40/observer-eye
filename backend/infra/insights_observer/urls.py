"""Insights Observer URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'insights_observer'

router = DefaultRouter()
router.register(r'insights', views.InsightViewSet, basename='insight')
router.register(r'anomalies', views.AnomalyDetectionViewSet, basename='anomaly')

urlpatterns = [
    path('', include(router.urls)),
]
