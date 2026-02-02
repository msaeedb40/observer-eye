"""Integration admin."""
from django.contrib import admin
from .models import Integration, DataSource, Webhook

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'integration_type', 'enabled', 'sync_status', 'last_sync']
    list_filter = ['integration_type', 'enabled']

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'integration', 'enabled', 'polling_interval']
    list_filter = ['source_type', 'enabled']

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['name', 'data_type', 'enabled', 'last_received']
    list_filter = ['data_type', 'enabled']
