"""Integration URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'integration'

router = DefaultRouter()
router.register(r'integrations', views.IntegrationViewSet, basename='integration')
router.register(r'datasources', views.DataSourceViewSet, basename='datasource')
router.register(r'webhooks', views.WebhookViewSet, basename='webhook')

urlpatterns = [
    path('', include(router.urls)),
]
