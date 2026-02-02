"""Analytics admin."""
from django.contrib import admin
from .models import Dashboard, Widget, Report, SavedQuery

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public', 'created_at']
    list_filter = ['is_public']
    search_fields = ['name']

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'dashboard', 'created_at']
    list_filter = ['widget_type']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'schedule', 'last_run']
    list_filter = ['report_type']

@admin.register(SavedQuery)
class SavedQueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'data_source', 'created_at']
    list_filter = ['data_source']
