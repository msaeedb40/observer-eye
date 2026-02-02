"""Template Dashboards serializers."""
from rest_framework import serializers
from .models import DashboardTemplate, TemplateInstance


class DashboardTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'downloads']


class DashboardTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardTemplate
        fields = ['id', 'name', 'description', 'category', 'thumbnail', 'is_official', 'downloads']


class TemplateInstanceSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = TemplateInstance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
