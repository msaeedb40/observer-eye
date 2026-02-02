"""Template Dashboards URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'template_dashboards'

router = DefaultRouter()
router.register(r'templates', views.DashboardTemplateViewSet, basename='dashboard-template')
router.register(r'instances', views.TemplateInstanceViewSet, basename='template-instance')

urlpatterns = [
    path('', include(router.urls)),
]
