"""Notification admin."""
from django.contrib import admin
from .models import NotificationChannel, AlertRule, Alert, NotificationHistory

@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_type', 'is_default', 'is_active']
    list_filter = ['channel_type', 'is_default']

@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'condition_type', 'enabled', 'evaluation_interval']
    list_filter = ['severity', 'enabled']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'severity', 'started_at', 'resolved_at']
    list_filter = ['state', 'severity']
    ordering = ['-started_at']

@admin.register(NotificationHistory)
class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = ['alert', 'channel', 'status', 'sent_at']
    list_filter = ['status']
