"""Settings URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'settings'

router = DefaultRouter()
router.register(r'settings', views.SettingViewSet, basename='setting')
router.register(r'preferences', views.UserPreferenceViewSet, basename='preference')
router.register(r'features', views.FeatureFlagViewSet, basename='feature-flag')
router.register(r'workspace', views.WorkspaceSettingsViewSet, basename='workspace')

urlpatterns = [
    path('', include(router.urls)),
]
