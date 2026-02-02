"""Integration serializers."""
from rest_framework import serializers
from .models import Integration, DataSource, Webhook


class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'last_sync', 'sync_status']
        extra_kwargs = {'credentials': {'write_only': True}}


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'token', 'last_received']
