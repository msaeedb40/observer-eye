"""Notification URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'notification'

router = DefaultRouter()
router.register(r'channels', views.NotificationChannelViewSet, basename='channel')
router.register(r'rules', views.AlertRuleViewSet, basename='alert-rule')
router.register(r'alerts', views.AlertViewSet, basename='alert')
router.register(r'history', views.NotificationHistoryViewSet, basename='notification-history')

urlpatterns = [
    path('', include(router.urls)),
]
