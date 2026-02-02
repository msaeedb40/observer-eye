"""Notification serializers."""
from rest_framework import serializers
from .models import NotificationChannel, AlertRule, Alert, NotificationHistory


class NotificationChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AlertRuleSerializer(serializers.ModelSerializer):
    channels = NotificationChannelSerializer(many=True, read_only=True)
    channel_ids = serializers.PrimaryKeyRelatedField(
        queryset=NotificationChannel.objects.all(),
        many=True,
        write_only=True,
        source='channels'
    )
    
    class Meta:
        model = AlertRule
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AlertSerializer(serializers.ModelSerializer):
    rule_name = serializers.CharField(source='rule.name', read_only=True)
    
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'started_at']


class NotificationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationHistory
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
