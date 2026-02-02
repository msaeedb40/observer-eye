"""Analytics serializers."""
from rest_framework import serializers
from .models import Dashboard, Widget, Report, SavedQuery


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class DashboardSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class DashboardListSerializer(serializers.ModelSerializer):
    widget_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dashboard
        fields = ['id', 'name', 'description', 'is_public', 'widget_count', 'created_at']
    
    def get_widget_count(self, obj):
        return obj.widgets.count()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'last_run']


class SavedQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedQuery
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
