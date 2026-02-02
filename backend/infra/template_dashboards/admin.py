"""Template Dashboards admin."""
from django.contrib import admin
from .models import DashboardTemplate, TemplateInstance

@admin.register(DashboardTemplate)
class DashboardTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_official', 'downloads', 'version']
    list_filter = ['category', 'is_official']

@admin.register(TemplateInstance)
class TemplateInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'template', 'user_id', 'created_at']
    list_filter = ['template']
