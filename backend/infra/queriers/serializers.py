"""Queriers serializers."""
from rest_framework import serializers
from .models import QueryTemplate, QueryExecution


class QueryTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class QueryExecutionSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = QueryExecution
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'executed_at', 'duration_ms', 'row_count', 'status', 'error_message']
