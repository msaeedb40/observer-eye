"""Analytics URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'analytics'

router = DefaultRouter()
router.register(r'dashboards', views.DashboardViewSet, basename='dashboard')
router.register(r'widgets', views.WidgetViewSet, basename='widget')
router.register(r'reports', views.ReportViewSet, basename='report')
router.register(r'queries', views.SavedQueryViewSet, basename='saved-query')

urlpatterns = [
    path('', include(router.urls)),
]
