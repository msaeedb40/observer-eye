"""Queriers admin."""
from django.contrib import admin
from .models import QueryTemplate, QueryExecution

@admin.register(QueryTemplate)
class QueryTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'data_type', 'query_language', 'created_at']
    list_filter = ['data_type', 'query_language']

@admin.register(QueryExecution)
class QueryExecutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'data_type', 'status', 'duration_ms', 'executed_at']
    list_filter = ['data_type', 'status']
    ordering = ['-executed_at']
