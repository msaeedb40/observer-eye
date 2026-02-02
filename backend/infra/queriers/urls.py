"""Queriers URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'queriers'

router = DefaultRouter()
router.register(r'templates', views.QueryTemplateViewSet, basename='query-template')
router.register(r'executions', views.QueryExecutionViewSet, basename='query-execution')

urlpatterns = [
    path('', include(router.urls)),
]
